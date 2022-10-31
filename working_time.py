import datetime

class WorkingTime:
    def __init__(self, start_time=None) -> None:
        self.working_time = datetime.timedelta(
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
        self.working_time += datetime.datetime.now() - self.start_time
        self.start_time = None
        self._is_working = False
    
    def start_working(self):
        self.start_time = datetime.datetime.now()
        self._is_working = True
        
    def reset_working_time(self):
        self.working_time = datetime.timedelta(
            days=0,
            seconds=0,
            microseconds=0,
            milliseconds=0,
            minutes=0,
            hours=0,
            weeks=0,
        )
    
    def __str__(self):
        working_total_seconds = int(self.working_time.total_seconds())
        working_total_hours = working_total_seconds // 3600
        working_minutes = working_total_seconds % 3600 // 60
        
        return "{0}H {1}M".format(working_total_hours, working_minutes)