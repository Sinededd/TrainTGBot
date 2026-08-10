from datetime import date, datetime

from dateutil import parser


def convert_to_iso(date_string) -> str | None:
    try:
        parsed_date = parser.parse(date_string, dayfirst=True)
        return parsed_date.strftime('%Y-%m-%d')
    except (ValueError, TypeError):
        return None


def convert_to_ddmmyyyy(date_string) -> str | None:
    try:
        parsed_date = parser.parse(date_string, dayfirst=True)
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
