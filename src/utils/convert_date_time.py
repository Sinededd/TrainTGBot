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


def get_datetime_iso(date: str, time: str) -> str:
    """Return datetime ISO formatted"""
    parsed_date = parser.parse(date, dayfirst=True)
    full_datetime = parser.parse(time, default=parsed_date)
    return full_datetime.isoformat()
