from typing import TypedDict, List
from datetime import datetime

#https://github.com/python/mypy/issues/5149
class Attendance(TypedDict):
    name: str
    dates: List[datetime]

class Course(TypedDict):
    day: str
    start_time: str
    finish_time: str
    grade: int
    attendance: Attendance
