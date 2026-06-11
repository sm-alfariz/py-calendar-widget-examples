from PyQt6.QtCore import QDate


class HolidayManager:
    def __init__(self):
        self.holidays = {
            QDate(2026, 1, 1): "Tahun Baru Masehi 2026",
            QDate(2026, 1, 16): "Isra Mi'raj Nabi Muhammad SAW",
            QDate(2026, 1, 19): "Tahun Baru Imlek 2577 Kongzili",
            QDate(2026, 1, 20): "Tahun Baru Imlek 2577 Kongzili",
            QDate(2026, 2, 26): "Mahasivarathri Day",
            QDate(2026, 3, 13): "Medin Full Moon Poya Day",
            QDate(2026, 3, 31): "Ramazan Festival Day",
            QDate(2026, 4, 12): "Bak Full Moon Poya Day",
            QDate(2026, 4, 13): "Day Before Sinhala & Tamil New Year Day",
            QDate(2026, 4, 14): "Sinhala & Tamil New Year Day",
            QDate(2026, 4, 15): "Special Bank Holiday",
            QDate(2026, 4, 18): "Good Friday",
            QDate(2026, 5, 1): "May Day",
            QDate(2026, 5, 12): "Vesak Full Moon Poya Day",
            QDate(2026, 5, 13): "Day following Vesak Full Moon Poya Day",
            QDate(2026, 6, 7): "Hadji Festival Day",
            QDate(2026, 6, 10): "Poson Full Moon Poya Day",
            QDate(2026, 7, 10): "Esala Full Moon Poya Day",
            QDate(2026, 8, 17): "Kemerdekaan RI",
            QDate(2026, 9, 5): "Holy Prophet's Birthday",
            QDate(2026, 9, 7): "Binara Full Moon Poya Day",
            QDate(2026, 10, 6): "Vap Full Moon Poya Day",
            QDate(2026, 10, 20): "Deepavali Festival Day",
            QDate(2026, 11, 5): "Ill Full Moon Poya Day",
            QDate(2026, 12, 4): "Unduvap Full Moon Poya Day",
            QDate(2026, 12, 25): "Christmas Day",
        }

    def get_holiday(self, date):
        return self.holidays.get(date, "No holidays")
