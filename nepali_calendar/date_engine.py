import datetime
import nepali_datetime
from nepali_datetime import _days_in_month

BS_MONTH_NAMES = [
    "बैशाख", "जेठ", "असार", "साउन", "भाद्र", "असोज",
    "कार्तिक", "मंसिर", "पुस", "माघ", "फाल्गुन", "चैत्र",
]

BS_MONTH_NAMES_EN = [
    "Baisakh", "Jestha", "Ashar", "Shrawan", "Bhadra", "Ashoj",
    "Kartik", "Mansir", "Poush", "Magh", "Falgun", "Chaitra",
]

AD_MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

AD_MONTH_SHORT = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]

WEEKDAY_NAMES_FULL_NP = [
    "आइतबार", "सोमबार", "मंगलबार", "बुधबार", "बिहिबार", "शुक्रबार", "शनिबार",
]

WEEKDAY_NAMES_SHORT_EN = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

_DEVA_DIGITS = "०१२३४५६७८९"


def to_devanagari(n: int) -> str:
    return "".join(_DEVA_DIGITS[int(d)] for d in str(n))


def format_number(n: int, lang: str) -> str:
    return to_devanagari(n) if lang == "np" else str(n)


def get_weekday_names(lang: str) -> list:
    return WEEKDAY_NAMES_FULL_NP if lang == "np" else WEEKDAY_NAMES_SHORT_EN


def get_today_bs() -> nepali_datetime.date:
    return nepali_datetime.date.today()


def get_days_in_month(bs_year: int, bs_month: int) -> int:
    return _days_in_month(bs_year, bs_month)


def bs_to_ad(bs_date: nepali_datetime.date) -> datetime.date:
    return bs_date.to_datetime_date()


def ad_to_bs(ad_date: datetime.date) -> nepali_datetime.date:
    return nepali_datetime.date.from_datetime_date(ad_date)


def get_first_weekday(bs_year: int, bs_month: int) -> int:
    """Return 0-based column index for the first day (0=Sunday, 6=Saturday)."""
    first_ad = nepali_datetime.date(bs_year, bs_month, 1).to_datetime_date()
    return (first_ad.weekday() + 1) % 7


def make_bs_date(year: int, month: int, day: int) -> nepali_datetime.date:
    return nepali_datetime.date(year, month, day)


def prev_month(bs_year: int, bs_month: int):
    if bs_month == 1:
        return bs_year - 1, 12
    return bs_year, bs_month - 1


def next_month(bs_year: int, bs_month: int):
    if bs_month == 12:
        return bs_year + 1, 1
    return bs_year, bs_month + 1


def get_week_start_ad(ref_ad: datetime.date) -> datetime.date:
    """Return the Sunday that starts the week containing ref_ad."""
    days_since_sun = (ref_ad.weekday() + 1) % 7
    return ref_ad - datetime.timedelta(days=days_since_sun)


def format_month_year_title(bs_year: int, bs_month: int, lang: str, cal_mode: str) -> str:
    if cal_mode == "bs":
        month = BS_MONTH_NAMES[bs_month - 1] if lang == "np" else BS_MONTH_NAMES_EN[bs_month - 1]
        year = to_devanagari(bs_year) if lang == "np" else str(bs_year)
        return f"{month} {year}"
    else:
        # Use mid-month day to pick the dominant AD month
        mid = get_days_in_month(bs_year, bs_month) // 2 + 1
        ad = nepali_datetime.date(bs_year, bs_month, mid).to_datetime_date()
        return f"{AD_MONTH_NAMES[ad.month - 1]} {ad.year}"


def format_year_title(bs_year: int, lang: str, cal_mode: str) -> str:
    if cal_mode == "bs":
        return to_devanagari(bs_year) if lang == "np" else str(bs_year)
    else:
        first_ad = nepali_datetime.date(bs_year, 1, 1).to_datetime_date()
        return str(first_ad.year)


def format_week_title(week_start_ad: datetime.date, lang: str, cal_mode: str) -> str:
    week_end_ad = week_start_ad + datetime.timedelta(days=6)
    if cal_mode == "bs":
        s = ad_to_bs(week_start_ad)
        e = ad_to_bs(week_end_ad)
        d1 = format_number(s.day, lang)
        d2 = format_number(e.day, lang)
        if s.month == e.month:
            m = BS_MONTH_NAMES[s.month - 1] if lang == "np" else BS_MONTH_NAMES_EN[s.month - 1]
            y = to_devanagari(s.year) if lang == "np" else str(s.year)
            return f"{m} {d1}–{d2}, {y}"
        else:
            m1 = BS_MONTH_NAMES[s.month - 1] if lang == "np" else BS_MONTH_NAMES_EN[s.month - 1]
            m2 = BS_MONTH_NAMES[e.month - 1] if lang == "np" else BS_MONTH_NAMES_EN[e.month - 1]
            return f"{m1} {d1} – {m2} {d2}"
    else:
        d1, d2 = week_start_ad.day, week_end_ad.day
        if week_start_ad.month == week_end_ad.month:
            m = AD_MONTH_NAMES[week_start_ad.month - 1]
            return f"{m} {d1}–{d2}, {week_start_ad.year}"
        else:
            m1 = AD_MONTH_SHORT[week_start_ad.month - 1]
            m2 = AD_MONTH_SHORT[week_end_ad.month - 1]
            return f"{m1} {d1} – {m2} {d2}"
