import time


def isTimeFormat(inputTime):
    try:
        time.strptime(str(inputTime), '%H:%M')
        return True
    except Exception as e:
        return False


def safeCastBool(val, default=False):
    try:
        return str(val).lower() in ['true', '1', 'y', 'yes']
    except Exception as e:
        return default
