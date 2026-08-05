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