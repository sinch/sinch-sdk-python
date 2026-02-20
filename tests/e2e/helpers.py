"""
Common utility helpers for E2E tests, shared across domains.
"""


def store_webhook_response(context, response):
    context.webhook_headers = dict(response.headers)
    context.raw_event = response.text


def has_key_or_attr(obj, key):
    if obj is None:
        return False
    if isinstance(obj, dict):
        return key in obj and obj[key] is not None
    return getattr(obj, key, None) is not None
