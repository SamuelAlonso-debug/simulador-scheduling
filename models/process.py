from dataclasses import dataclass

@dataclass
class Process:
    pid: str
    arrival_time: int
    burst_time: int
    remaining_time: int
    queue_level: int  # 0 = mayor prioridad

@dataclass
class GanttEntry:
    pid: str
    start: int
    end: int