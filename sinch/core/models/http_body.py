import json
import mimetypes
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, BinaryIO, Mapping, Optional, Sequence, Union
from urllib.parse import urlencode
from uuid import uuid4

FormScalar = Union[str, bytes, int, float, bool]
FormValue = Optional[Union[FormScalar, Sequence[FormScalar]]]


class HttpBody(ABC):
    """
    Request body encoded by the SDK into the bytes sent on the wire.
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
    Request body sent form-urlencoded. A list value is sent as a repeated field and a ``None`` value is omitted.

    :param fields: The form fields, keyed by field name.
    :type fields: Mapping[str, Optional[Union[str, bytes, int, float, bool, Sequence[Union[str, bytes, int, float, bool]]]]]
    """

    content_type = "application/x-www-form-urlencoded"

    def __init__(self, fields: Mapping[str, FormValue]) -> None:
        self.fields = fields

    def encode(self) -> bytes:
        fields = [(name, value) for name, value in self.fields.items() if value is not None]
        return urlencode(fields, doseq=True).encode("utf-8")

    def __repr__(self) -> str:
        return f"UrlEncodedBody({self.fields!r})"


class FilePart(HttpBody):
    """
    File sent as the whole request body, or as a part of a :class:`MultipartBody`.

    :param content: The file content: bytes, a binary file object or the path of a file, read when the body is encoded.
        A file object is consumed by the read, so it cannot be shared between bodies.
    :type content: Union[bytes, BinaryIO, Path]
    :param filename: The file name sent to the server in a :class:`MultipartBody`. Defaults to the name of a path;
        otherwise the field name is sent.
    :type filename: Optional[str]
    :param content_type: The media type of the file. Guessed from the file name if omitted, or
        ``application/octet-stream`` if it cannot be guessed.
    :type content_type: Optional[str]
    :raises ValueError: If ``content`` is not a supported type or ``content_type`` contains a line break.
    """

    def __init__(
        self,
        content: Union[bytes, BinaryIO, Path],
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> None:
        if not isinstance(content, (bytes, Path)) and not hasattr(content, "read"):
            raise ValueError(
                f"content must be bytes, a binary file object or a Path, got: {type(content).__name__}"
            )
        _reject_line_breaks("content_type", content_type)
        self.content = content
        self.filename = filename or (content.name if isinstance(content, Path) else None)
        self.content_type = (
            content_type
            or mimetypes.guess_type(self.filename or "")[0]
            or "application/octet-stream"
        )

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

    def encode(self) -> bytes:
        return self.read()

    def __repr__(self) -> str:
        return f"FilePart(filename={self.filename!r}, content_type={self.content_type!r})"


MultipartValue = Optional[Union[FormScalar, FilePart, Sequence[Union[FormScalar, FilePart]]]]


class MultipartBody(HttpBody):
    """
    Request body sent as ``multipart/form-data``, built in memory.

    The boundary is generated when the body is created and is part of :attr:`content_type`.

    :param fields: The parts, keyed by field name and sent in the given order. A :class:`FilePart` is sent as a file
        and a value that is not ``bytes`` as its ``str``. A list value is sent as a repeated field, and it can mix
        files and other values. A ``None`` value is omitted.
    :type fields: Optional[Mapping[str, Optional[Union[str, bytes, int, float, bool, FilePart, Sequence[Union[str, bytes, int, float, bool, FilePart]]]]]]
    """

    def __init__(self, fields: Optional[Mapping[str, MultipartValue]] = None) -> None:
        self.fields = fields or {}
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
            for item in [value] if isinstance(value, (str, bytes)) or not isinstance(value, Sequence) else value:
                chunks.append(delimiter + _encode_part(name, item))
        return b"".join(chunks) + f"--{self.boundary}--\r\n".encode("ascii")

    def __repr__(self) -> str:
        return f"MultipartBody(fields={list(self.fields)!r})"


def _encode_part(name: str, item: Union[FormScalar, FilePart]) -> bytes:
    disposition = f'Content-Disposition: form-data; name="{_escape_quoted(name)}"'
    if isinstance(item, FilePart):
        headers = (
            f'{disposition}; filename="{_escape_quoted(item.filename or name)}"\r\n'
            f"Content-Type: {item.content_type}\r\n\r\n"
        )
        return headers.encode("utf-8") + item.read() + b"\r\n"
    data = item if isinstance(item, bytes) else str(item).encode("utf-8")
    return f"{disposition}\r\n\r\n".encode("utf-8") + data + b"\r\n"


def _escape_quoted(value: str) -> str:
    return value.replace('"', "%22").replace("\r", "%0D").replace("\n", "%0A")


def _reject_line_breaks(name: str, value: Optional[str]) -> None:
    if value and ("\r" in value or "\n" in value):
        raise ValueError(f"{name} must not contain line breaks")
