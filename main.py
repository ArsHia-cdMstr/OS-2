from dataclasses import dataclass
from enum import Enum


# Note : define the Resources data class (struct)
@dataclass
class Resource:
    number: int


R1 = Resource(0)
R2 = Resource(0)
R3 = Resource(0)


# Note : define the type of tasks dataclass and then initial them
@dataclass
class Task_type:
    priority: int
    resource_type: list[Resource]


x = Task_type(3, [R1, R2])
y = Task_type(2, [R2, R3])
z = Task_type(1, [R1, R3])


# here we will define an enum to determine the status of a process
class Status(Enum):
    running = 0
    ready = 1
    waiting = 2


class Process:

    def __init__(self, name, task_type, status, arrival_time, burst_time):
        self.name: str = name
        self.task_type: Task_type = task_type
        self.status: Status = status
        self.arrival_time: int = arrival_time
        self.burst_time: int = burst_time
