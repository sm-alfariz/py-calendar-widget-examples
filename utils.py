from PyQt6.QtCore import QLocale, QDate


def indonesia_date(format_date="long", date=QDate.currentDate()):
    """Formats a date according to the Indonesian locale."""
    """QDate is used to represent the date, and QLocale handles the localization aspects."""
    """format_date can be 'long', 'short', or 'custom' to specify the desired date format."""
    locale_id = QLocale(QLocale.Language.Indonesian, QLocale.Country.Indonesia)
    formatted_long = locale_id.toString(date, QLocale.FormatType.LongFormat)

    # Format the date according to the locale's short format
    formatted_short = locale_id.toString(date, QLocale.FormatType.ShortFormat)
    # date only
    formatted_date_only = locale_id.toString(date, "dddd")
    # Custom format using locale (e.g., day name + date)
    formatted_custom = locale_id.toString(date, "dddd, dd MMMM yyyy")
    if format_date == "long":
        return formatted_long
    elif format_date == "short":
        return formatted_short
    elif format_date == "custom":
        return formatted_custom
    elif format_date == "date_only":
        return locale_id.toString(date, "dddd")
    else :
        return formatted_long  # Default to long format if an unknown option is provided

def indonesia_date_month(date=QDate.currentDate(), format_date="short"):

    """Formats a date to show only the month and year in Indonesian locale."""
    
    locale_id = QLocale(QLocale.Language.Indonesian, QLocale.Country.Indonesia)
    if format_date == "short":
        formatted_month_year =locale_id.toString(date, "MMM")
    else:
        formatted_month_year = locale_id.toString(date, "MMMM")
    return formatted_month_year

tgl = indonesia_date(format_date="date_only")
print(tgl)