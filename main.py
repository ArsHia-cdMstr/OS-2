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


class Task:

    def __init__(self, name, task_type, status, arrival_time, burst_time):
        self.name: str = name
        self.task_type: Task_type = task_type
        self.status: Status = status
        self.arrival_time: int = arrival_time
        self.burst_time: int = burst_time


class Scheduler:
    ready_Q: list[Task]
    waiting_Q: list[Task]
    current_time = 0

    def __init__(self):
        self.ready_Q = []
        self.waiting_Q = []

    def add_to_readyQ(self, process):
        self.ready_Q.append(process)

    def add_to_waitingQ(self, process):
        self.ready_Q.remove(process)
        self.waiting_Q.append(process)

    def assign_process_by_priority(self):
        self.ready_Q.sort(key=lambda proc: proc.task.task_type.priority)
        chased_process: Task or None = self.ready_Q[0]
        return chased_process

    def update_queues(self):
        pass

    def start(self):
        while self.run():
            pass

    def run(self):
        task = self.assign_process_by_priority()

        # todo: check for the resources

        # if task isn't none
        if not task:
            self.current_time += task.burst_time
        else:
            self.current_time += 1

        # todo: free resources
        # todo: update ready queue
