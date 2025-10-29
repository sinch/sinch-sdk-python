def model_dump_for_query_params(model, exclude_none=True, by_alias=True):
    """
    Serializes a Pydantic model for use as query parameters.
    Converts list values to comma-separated strings for APIs that expect this format.
    Filters out empty values (empty strings and empty lists).
    
    Args:
        model: A Pydantic BaseModel instance
        exclude_none: Whether to exclude None values (default: True)
        by_alias: Whether to use field aliases (default: True)
        
    Returns:
        dict: Serialized model data with lists converted to comma-separated strings
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

