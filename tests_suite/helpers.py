import datetime

available_units = {
    'hour': 'hours',
    'day': 'days',
    'week': 'weeks',
    'month': 'months'
}

timezone = +2.0
date_timezone = datetime.timezone(datetime.timedelta(hours=timezone))

def time_difference(dateofbirth, unit):
    if unit not in available_units.keys():
        raise AttributeError(f'Given unit not valid. Available units: {available_units}')

    dateofbirth = datetime.datetime.strptime(dateofbirth, "%Y-%m-%d").replace(tzinfo=date_timezone)
    now = datetime.datetime.now(date_timezone)

    next_birthday = dateofbirth.replace(year=now.year)
    if now.date() > next_birthday.date():
        next_birthday = dateofbirth.replace(year=now.year + 1)

    res_in_hours = int((next_birthday - now).total_seconds() // 3600)
    res_in_hours = 0 if res_in_hours < 0 else res_in_hours  # If birthday is today, hours will be negative, but cant be

    if unit == "day":
        return int(res_in_hours // 24)
    elif unit == "week":
        return int(res_in_hours // (24 * 7))
    elif unit == "month":
        return int(res_in_hours // (24 * 30))
    else:
        return res_in_hours


def get_standard_result_message(dateofbirth, unit):
    return f'{time_difference(dateofbirth, unit)} {available_units[unit]} left'
