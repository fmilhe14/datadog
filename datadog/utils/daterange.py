import datetime


def daterange(date1, date2):
    """
    This method will return an iterator with all the date between date1 and date 2.
    :param date1: datetime
    :param date2: datetime
    :return: Iterator<datetime>
    """
    delta = (date2 - date1).total_seconds()/3600
    for i in range(int(delta) + 1):
        yield date1 + datetime.timedelta(hours=i)
