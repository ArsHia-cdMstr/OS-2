from dataclasses import dataclass
from enum import Enum


# Note : define the Resources data class (struct)
@dataclass
class Resource:
    name: str


R1 = Resource("R1")
R2 = Resource("R2")
R3 = Resource("R3")


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


class AlgoModel(Enum):
    FCFS = 'First Come First Serve'
    RR = 'Round Robin'
    SJF = 'shortest job first'
    HRRN = 'highest response ratio next'


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
    resource: dict[Resource, int]
    running_task_name: str

    def __init__(self):
        self.ready_Q = []
        self.waiting_Q = []

    def __str__(self):
        for res, res_number in self.resource.items():
            print(f"{res.name}: {res_number}\t", end='')

        print(f"\npriority queue: {self.ready_Q}")
        print(f"waiting queue: {self.waiting_Q}")

    def add_to_readyQ(self, process):
        self.ready_Q.append(process)

    def add_to_waitingQ(self, process):
        self.ready_Q.remove(process)
        self.waiting_Q.append(process)

    def assign_process_by_priority(self):
        self.ready_Q.sort(key=lambda proc: proc.task.task_type.priority, reverse=True)
        chased_process: Task or None = self.ready_Q.pop()
        return chased_process

    # todo : work on this method
    def assign_process(self, assign_type=AlgoModel.FCFS):
        return self.assign_process_by_priority()

    # todo: add a func to initial resources number
    def update_queues(self):
        pass

    def can_use_resources(self, task: Task):
        satisfy = False
        for res in task.task_type.resource_type:
            if self.resource[res] < 1:
                return satisfy

        satisfy = True
        for res in task.task_type.resource_type:
            self.resource[res] -= 1

        return satisfy

    def chose_task(self, algo_type=AlgoModel.FCFS):
        task = self.assign_process(algo_type)
        while not self.can_use_resources(task):
            self.add_to_waitingQ(task)
            task = self.assign_process(algo_type)
        self.running_task_name = task.name
        return task

    def run_FCFS(self, task: Task):
        for i in range(task.burst_time):
            self.current_time += 1
            print(self)

    def run(self, algo_type=AlgoModel.FCFS):
        task = self.chose_task()

        if algo_type == AlgoModel.FCFS:
            self.run_FCFS()

        # todo: free resources
        # todo: update ready queue

    def start(self):
        while self.run():
            pass
