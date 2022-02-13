from datetime import datetime

def time_checker():
    # get current time
    working_days = [0, 1, 2, 3, 4]  # monday to friday
    now = datetime.now()
    # check if during operational hours
    if datetime.today().weekday() not in working_days:
        return "Stock markets are not open on weekends."
    if datetime.now().hour < 17 or datetime.now().hour > 23:
        return "U.S market is closed."

    return "U.S market is currently open."

