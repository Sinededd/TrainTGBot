from datetime import date, datetime

from dateutil import parser


def convert_to_iso(date_string: str | date | datetime) -> str | None:
    """Convert a date string or date/datetime object to ISO YYYY-MM-DD string.

    Accepts either a string (like '01.02.2026' or '2026-02-01') or a
    date/datetime object. Returns None on parse/convert failure.
    """
    try:
        if isinstance(date_string, (date, datetime)):
            return date_string.strftime('%Y-%m-%d')

        parsed_date = parser.parse(str(date_string), dayfirst=True)
        return parsed_date.strftime('%Y-%m-%d')
    except (ValueError, TypeError):
        return None


def convert_to_ddmmyyyy(date_string: str | date | datetime) -> str | None:
    """Convert a date string or date/datetime object to DD.MM.YYYY string.

    This now supports already-parsed date/datetime objects (which previously
    caused parse to raise and return None).
    """
    try:
        if isinstance(date_string, (date, datetime)):
            return date_string.strftime('%d.%m.%Y')

        parsed_date = parser.parse(str(date_string), dayfirst=True)
        return parsed_date.strftime('%d.%m.%Y')
    except (ValueError, TypeError):
        return None


def get_datetime_iso(date_val: str | date, time_val: str) -> str:
    """Return datetime ISO formatted"""
    if isinstance(date_val, (date, datetime)):
        date_str = date_val.strftime("%Y-%m-%d")
    else:
        date_str = str(date_val)

    parsed_date = parser.parse(date_str, dayfirst=True)
    full_datetime = parser.parse(time_val, default=parsed_date)
    return full_datetime.isoformat()
