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
        return locale_id.toString(date, "MMM")
    return locale_id.toString(date, "MMMM")


def get_theme_palette(theme="light"):
    theme = theme.lower()
    light = {
        "container_bg": "rgba(255, 255, 255, 0.92)",
        "text_color": "#333333",
        "accent_color": "#5DADE2",
        "accent_text": "#ffffff",
        "secondary_text": "rgb(128, 145, 146)",
        "date_text": "#5DADE2",
        "active_date_text": "#ffffff",
        "active_date_bg": "#5DADE2",
        "close_button_bg": "rgba(255, 107, 107, 0.7)",
        "close_button_text": "#ffffff",
        "close_button_hover": "rgba(255, 71, 87, 0.85)",
        "holiday_text": "rgb(224, 52, 32)",
        "holiday_bg": "rgba(236, 220, 96, 0.6)",
        "full_date_text": "rgb(17, 17, 17)",
        "shadow_color": "rgba(0, 0, 0, 40)",
        "nav_button_color": "#5DADE2",
        "nav_button_hover": "#3498DB",
    }
    dark = {
        "container_bg": "rgba(34, 39, 46, 0.94)",
        "text_color": "#f1f2f6",
        "accent_color": "#4da6ff",
        "accent_text": "#ffffff",
        "secondary_text": "#dcdde1",
        "date_text": "#4da6ff",
        "active_date_text": "#1e272e",
        "active_date_bg": "#4da6ff",
        "close_button_bg": "rgba(255, 107, 107, 0.5)",
        "close_button_text": "#ffffff",
        "close_button_hover": "rgba(255, 71, 87, 0.9)",
        "holiday_text": "#ffeaa7",
        "holiday_bg": "rgba(231, 76, 60, 0.18)",
        "full_date_text": "#dcdde1",
        "shadow_color": "rgba(0, 0, 0, 85)",
        "nav_button_color": "#4da6ff",
        "nav_button_hover": "#74b9ff",
    }
    return dark if theme == "dark" else light