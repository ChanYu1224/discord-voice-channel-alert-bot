import datetime

class WorkingTime:
    def __init__(self, start_time=None) -> None:
        self._weekly_working_time = datetime.timedelta(
            days=0,
            seconds=0,
            microseconds=0,
            milliseconds=0,
            minutes=0,
            hours=0,
            weeks=0,
        )
        self._daily_working_time = datetime.timedelta(
            days=0,
            seconds=0,
            microseconds=0,
            milliseconds=0,
            minutes=0,
            hours=0,
            weeks=0,
        )
        
        # about working time calculation
        self.start_time = start_time
        self._is_working = False
    
    def is_working(self):
        return self._is_working
    
    def end_working(self):
        self._weekly_working_time += datetime.datetime.now() - self.start_time
        self._daily_working_time += datetime.datetime.now() - self.start_time
        self.start_time = None
        self._is_working = False
    
    def start_working(self):
        self.start_time = datetime.datetime.now()
        self._is_working = True
        
    def reset_weekly_working_time(self):
        self._weekly_working_time = datetime.timedelta(
            days=0,
            seconds=0,
            microseconds=0,
            milliseconds=0,
            minutes=0,
            hours=0,
            weeks=0,
        )
    
    def reset_daily_working_time(self):
        self._daily_working_time = datetime.timedelta(
            days=0,
            seconds=0,
            microseconds=0,
            milliseconds=0,
            minutes=0,
            hours=0,
            weeks=0,
        )
    
    def get_weekly_working_time(self):
        return self.weekly_working_time

    def get_weekly_working_time_str(self):
        working_total_seconds = int(self._weekly_working_time.total_seconds())
        working_total_hours = working_total_seconds // 3600
        working_minutes = working_total_seconds % 3600 // 60
        
        return "{0:0=2}H{1:0=2}M".format(working_total_hours, working_minutes)

    def get_daily_working_time(self):
        return self._daily_working_time
    
    def get_daily_working_time_str(self):
        working_total_seconds = int(self._daily_working_time.total_seconds())
        working_total_hours = working_total_seconds // 3600
        working_minutes = working_total_seconds % 3600 // 60
        
        return "{0:0=2}H{1:0=2}M".format(working_total_hours, working_minutes)