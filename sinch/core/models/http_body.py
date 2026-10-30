import json
import mimetypes
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, BinaryIO, Mapping, Optional, Sequence, Union
from urllib.parse import urlencode
from uuid import uuid4


class HttpBody(ABC):
    """
    Request body built by an endpoint, encoded by the SDK into the bytes sent on the wire.
    """

    #: The ``Content-Type`` header sent with the body.
    content_type: str

    @abstractmethod
    def encode(self) -> bytes:
        """
        Returns the body as sent on the wire.

        :returns: The encoded body.
        :rtype: bytes
        """


class JsonBody(HttpBody):
    """
    Request body sent as JSON.

    :param data: The JSON-serializable body.
    :type data: Any
    """

    content_type = "application/json"

    def __init__(self, data: Any) -> None:
        self.data = data

    def encode(self) -> bytes:
        return json.dumps(self.data).encode("utf-8")

    def __repr__(self) -> str:
        return f"JsonBody({self.data!r})"


class UrlEncodedBody(HttpBody):
    """
    Request body sent form-urlencoded. A list value is sent as a repeated field.

    :param fields: The form fields, keyed by field name.
    :type fields: Mapping[str, Any]
    """

    content_type = "application/x-www-form-urlencoded"

    def __init__(self, fields: Mapping[str, Any]) -> None:
        self.fields = fields

    def encode(self) -> bytes:
        return urlencode(list(self.fields.items()), doseq=True).encode("utf-8")

    def __repr__(self) -> str:
        return f"UrlEncodedBody({self.fields!r})"


class FilePart:
    """
    File sent as a part of a :class:`MultipartBody`.

    :param content: The file content: bytes, a binary file object or the path of a file, read when the body is encoded.
    :type content: Union[bytes, BinaryIO, Path]
    :param filename: The file name sent to the server.
    :type filename: str
    :param content_type: The media type of the file. Guessed from ``filename`` if omitted, or
        ``application/octet-stream`` if it cannot be guessed.
    :type content_type: Optional[str]
    :raises ValueError: If ``content_type`` contains a line break.
    """

    def __init__(
        self,
        content: Union[bytes, BinaryIO, Path],
        filename: str,
        content_type: Optional[str] = None,
    ) -> None:
        _reject_line_breaks("content_type", content_type)
        self.content = content
        self.filename = filename
        self.content_type = content_type or mimetypes.guess_type(filename)[0] or "application/octet-stream"

    def read(self) -> bytes:
        """
        Returns the file content.

        :returns: The file bytes.
        :rtype: bytes
        """
        if isinstance(self.content, bytes):
            return self.content
        if isinstance(self.content, Path):
            return self.content.read_bytes()
        return self.content.read()

    def __repr__(self) -> str:
        return f"FilePart(filename={self.filename!r}, content_type={self.content_type!r})"


class MultipartBody(HttpBody):
    """
    Request body sent as ``multipart/form-data``, built in memory.

    The boundary is generated when the body is created and is part of :attr:`content_type`.

    :param fields: The text fields, keyed by field name. A value that is not ``bytes`` is sent as its ``str``,
        and a ``None`` value is omitted.
    :type fields: Optional[Mapping[str, Any]]
    :param files: The files, keyed by field name. A list sends several files under the same name.
    :type files: Optional[Mapping[str, Union[FilePart, Sequence[FilePart]]]]
    """

    def __init__(
        self,
        fields: Optional[Mapping[str, Any]] = None,
        files: Optional[Mapping[str, Union[FilePart, Sequence[FilePart]]]] = None,
    ) -> None:
        self.fields = fields or {}
        self.files = files or {}
        self.boundary = uuid4().hex
        self.content_type = f"multipart/form-data; boundary={self.boundary}"
        self._encoded: Optional[bytes] = None

    def encode(self) -> bytes:
        if self._encoded is None:
            self._encoded = self._build()
        return self._encoded

    def _build(self) -> bytes:
        # urllib3.filepost.encode_multipart_formdata could replace this encoder.
        # It is not used because urllib3 is not a direct dependency
        # and its header escaping changes between urllib3 versions.
        delimiter = f"--{self.boundary}\r\n".encode("ascii")
        chunks = []
        for name, value in self.fields.items():
            if value is None:
                continue
            data = value if isinstance(value, bytes) else str(value).encode("utf-8")
            disposition = f'Content-Disposition: form-data; name="{_escape_quoted(name)}"'
            chunks.append(delimiter + f"{disposition}\r\n\r\n".encode("utf-8") + data + b"\r\n")
        for name, parts in self.files.items():
            for part in [parts] if isinstance(parts, FilePart) else parts:
                disposition = (
                    f'Content-Disposition: form-data; name="{_escape_quoted(name)}"; '
                    f'filename="{_escape_quoted(part.filename)}"'
                )
                headers = f"{disposition}\r\nContent-Type: {part.content_type}\r\n\r\n"
                chunks.append(delimiter + headers.encode("utf-8") + part.read() + b"\r\n")
        return b"".join(chunks) + f"--{self.boundary}--\r\n".encode("ascii")

    def __repr__(self) -> str:
        return f"MultipartBody(fields={list(self.fields)!r}, files={list(self.files)!r})"


def _escape_quoted(value: str) -> str:
    return value.replace('"', "%22").replace("\r", "%0D").replace("\n", "%0A")


def _reject_line_breaks(name: str, value: Optional[str]) -> None:
    if value and ("\r" in value or "\n" in value):
        raise ValueError(f"{name} must not contain line breaks")
