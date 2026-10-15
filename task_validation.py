"""Pure validation rules for the task domain; independent of Flask/API."""
from datetime import date

VALID_STATUSES = frozenset({'pending', 'completed'})
MAX_TITLE_LENGTH = 100


def validate_title(title):
    """Return stripped title or raise ValueError/TypeError for invalid input."""
    if not isinstance(title, str):
        raise TypeError('title must be a string')
    result = title.strip()
    if not result:
        raise ValueError('title is required')
    if len(result) > MAX_TITLE_LENGTH:
        raise ValueError('title must be at most 100 characters')
    return result


def validate_due_date(due_date):
    """Return canonical YYYY-MM-DD date string; past dates are permitted."""
    if not isinstance(due_date, str):
        raise TypeError('due_date must be a string')
    try:
        parsed = date.fromisoformat(due_date)
    except ValueError as exc:
        raise ValueError('due_date must be a valid YYYY-MM-DD date') from exc
    if parsed.isoformat() != due_date:
        raise ValueError('due_date must use YYYY-MM-DD format')
    return due_date


def validate_status(status):
    if not isinstance(status, str) or status not in VALID_STATUSES:
        raise ValueError('status must be pending or completed')
    return status
