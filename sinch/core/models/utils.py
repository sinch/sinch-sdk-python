from datetime import datetime, date
from typing import Optional, Dict, Any


def serialize_datetime_in_dict(value: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Serialize datetime/date objects in a dictionary to ISO 8601 date strings.
    
    :param value: Optional dictionary that may contain datetime/date objects
    :type value: Optional[Dict[str, Any]]
    :returns: Dictionary with datetime/date objects converted to ISO 8601 date strings,
              or None if input is None
    :rtype: Optional[Dict[str, Any]]
    """
    if value is None:
        return None
    
    serialized = {}
    for key, val in value.items():
        if isinstance(val, (datetime, date)):
            # Convert datetime/date to ISO 8601 date format (YYYY-MM-DD)
            if isinstance(val, datetime):
                serialized[key] = val.date().isoformat()
            else:
                serialized[key] = val.isoformat()
        else:
            # Pass string values directly to the backend without modification
            serialized[key] = val
    return serialized


def model_dump_for_query_params(model, exclude_none=True, by_alias=True):
    """
    Serializes a Pydantic model for use as query parameters.
    Converts list values to comma-separated strings for APIs that expect this format.
    Filters out empty values (empty strings and empty lists).
    
    :param model: A Pydantic BaseModel instance
    :type model: BaseModel
    :param exclude_none: Whether to exclude None values (default: True)
    :type exclude_none: bool
    :param by_alias: Whether to use field aliases (default: True)
    :type by_alias: bool
    :returns: Serialized model data with lists converted to comma-separated strings
    :rtype: dict
    """
    data = model.model_dump(exclude_none=exclude_none, by_alias=by_alias)
    filtered_data = {}
    for key, value in data.items():
        # Filter out empty strings
        if value == "":
            continue
        # Filter out empty lists
        if isinstance(value, list) and len(value) == 0:
            continue
        # Convert lists to comma-separated strings
        if isinstance(value, list):
            filtered_data[key] = ",".join(str(item) for item in value)
        else:
            filtered_data[key] = value
    return filtered_data
