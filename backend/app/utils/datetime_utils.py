from datetime import datetime, date, timedelta

def parse_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()

def format_datetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S') if dt else None

def get_month_range(month, year):
    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)
    return first_day, last_day