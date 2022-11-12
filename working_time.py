import datetime
from typing import List, Dict

class WorkingTime:
    def __init__(self, start_time=None) -> None:
        self._working_time = datetime.timedelta(
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
    
    def is_working(self) -> None:
        return self._is_working
    
    def end_working(self) -> None:
        self._working_time += datetime.datetime.now() - self.start_time
        self.start_time = None
        self._is_working = False
    
    def start_working(self) -> None:
        self.start_time = datetime.datetime.now()
        self._is_working = True
        
    def reset_working_time(self) -> None:
        self._working_time = datetime.timedelta(
            days=0,
            seconds=0,
            microseconds=0,
            milliseconds=0,
            minutes=0,
            hours=0,
            weeks=0,
        )
    
    def get_working_time(self) -> None:
        return self._working_time

    def __str__(self) -> str:
        working_total_seconds = int(self._working_time.total_seconds())
        working_total_hours = working_total_seconds // 3600
        working_minutes = working_total_seconds % 3600 // 60
        
        return "{0:0=2}H{1:0=2}M".format(working_total_hours, working_minutes)


class WorkingRecords:
    def __init__(self) -> None:
        self.working_time_dict: Dict[str, WorkingTime] = {}
    
    def reset_records(self,) -> None:
        new_working_time_dict = {}
        for user_name, working_time in self.working_time_dict.items():
            if working_time.is_working():
                working_time.reset_working_time()
                working_time.start_working()
                new_working_time_dict[user_name] = working_time
        self.working_time_dict = new_working_time_dict
    
    def start_record(self, user_name:str) -> None:
        if not user_name in self.working_time_dict.keys():
            self.working_time_dict[user_name] = WorkingTime()
            
        if self.working_time_dict[user_name].is_working():
            return
        else:
            self.working_time_dict[user_name].start_working()
    
    def stop_record(self, user_name:str) -> None:
        if user_name in self.working_time_dict.keys() and self.working_time_dict[user_name].is_working():
            self.working_time_dict[user_name].end_working()
    
    def get_sorted_working_records(self) -> str:
        # shape of [(user_name, working_time), ...]
        for user_name in self.working_time_dict.keys():
            if self.working_time_dict[user_name].is_working():
                self.stop_record(user_name)
                self.start_record(user_name)
        
        working_times_sorted: List[tuple] = sorted(
            self.working_time_dict.items(),
            key=lambda x:x[1].get_working_time(),
        )
        working_times_str = "```\n"
        if len(working_times_sorted) == 0:
            working_times_str += "No one worked..."
        else:
            for working_time in working_times_sorted:
                working_times_str += "{0}\t{1}\n".format(working_time[0], working_time[1])
        working_times_str += "```"
        
        return working_times_str
