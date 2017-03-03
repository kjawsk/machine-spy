import datetime

class MyDate():
    # it is wrapper for datetime.datetime.now() for test purposes
    @staticmethod
    def now():
        return datetime.datetime.now()
