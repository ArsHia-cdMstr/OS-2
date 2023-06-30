from dataclasses import dataclass
from enum import Enum


# Note : define the Resources data class (struct)
# @dataclass
# class Resource:
#     name: str

class Resource:
    def __init__(self, name: str):
        self.name = name

    # def __hash__(self):
    #     return hash(self.name)


R1 = Resource("R1")
R2 = Resource("R2")
R3 = Resource("R3")


# Note : define the type of tasks dataclass and then initial them
@dataclass
class Task_type:
    name: str
    priority: int
    resource_type: list[Resource]


x = Task_type('x', 3, [R1, R2])
y = Task_type('y', 2, [R2, R3])
z = Task_type('z', 1, [R1, R3])


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
    _waiting_Q: list[Task]
    _running_task_name: str or None

    def __init__(self, resource: dict[Resource, int], tasks_list: list[Task], alogorithm_type: AlgoModel):
        self.resource = resource
        self.ready_Q = tasks_list
        self._waiting_Q: list[Task] = []
        self.current_time = 0
        self.Algorithm_type = alogorithm_type

    def __str__(self):
        output = ""
        output += f"time : {self.current_time} sec \n"
        for res, res_number in self.resource.items():
            output += f"{res.name}: {res_number}\t"

        output += f"\nRunning task : {self._running_task_name}\n"

        readyQ_task_str = "[ "
        waitingQ_task_str = "[ "
        for task in self.ready_Q:
            readyQ_task_str += task.name + " "
        for task in self._waiting_Q:
            waitingQ_task_str += task.name + " "

        output += f"ready queue: {readyQ_task_str}]\n"
        output += f"waiting queue: {waitingQ_task_str}]\n"

        return output

    def _add_to_readyQ(self, process):
        self.ready_Q.append(process)

    def _add_to_waitingQ(self, process):
        self.ready_Q.remove(process)
        self._waiting_Q.append(process)

    def _assign_process_by_priority(self):
        self.ready_Q.sort(key=lambda x: x.task_type.priority, reverse=True)
        chased_process: Task or None = self.ready_Q.pop()
        return chased_process

    # todo : work on this method
    def _assign_process(self, assign_type=AlgoModel.FCFS):
        return self._assign_process_by_priority()

    def _can_use_resources(self, task1: Task):
        satisfy = False
        for res in task1.task_type.resource_type:
            if self.resource[res] < 1:
                return satisfy

        satisfy = True
        for res in task1.task_type.resource_type:
            self.resource[res] -= 1

        return satisfy

    def _chose_task(self, algo_type=AlgoModel.FCFS):

        if len(self.ready_Q) == 0:
            if len(self._waiting_Q) == 0:
                print("*********    tasks done succesfuly   **********")
                exit(0)
            else:
                print("_________________ deadlock accured __________________")
                exit(1)

        task = self._assign_process(algo_type)
        while not self._can_use_resources(task) and len(self.ready_Q) > 0:
            self._add_to_waitingQ(task)
            task = self._assign_process(algo_type)

        self._running_task_name = task.name
        return task

    def _run_FCFS(self, task: Task):
        for i in range(task.burst_time):
            print(self)
            self.current_time += 1
        print(self)

    def _free_resources(self, task: Task):
        for res in task.task_type.resource_type:
            self.resource[res] += 1

    def _update_queues(self):
        for task in self._waiting_Q:
            for res in task.task_type.resource_type:
                if self.resource[res] > 0:
                    self._waiting_Q.remove(task)
                    self._add_to_readyQ()

    def _run(self, algo_type=AlgoModel.FCFS):
        task = self._chose_task()

        if algo_type == AlgoModel.FCFS:
            self._run_FCFS(task)

        self._free_resources(task)
        self._running_task_name = None
        self._update_queues()
        print("after resource free up : ________________")
        print(self)

    def start(self):
        while True:
            self._run(self.Algorithm_type)


# r1_number, r2_number, r3_number = [int(x) for x in input("inter number of R1, R2, R3 resources: ").split()]
# task_num = int(input("inter number of tasks: "))
#
# task_list = []
#
# for _ in range(task_num):
#     task = input("inter \'task name\', \'task type\', \'task duration\' : ").split()
#     task_type: Task_type
#     if task[1] == 'x':
#         task_type = x
#     if task[1] == 'y':
#         task_type = y
#     else:
#         task_type = z
#
#     task_list.append(Task(task[0], task_type, Status.ready, 0, int(task[2])))
#
# reso = {
#     "R1": r1_number,
#     "R2": r2_number,
#     "R3": r3_number}


# Note: this is a test
task_list = []

task_list.append(Task('t1', y, Status.ready, 0, 3))
task_list.append(Task('t2', x, Status.ready, 0, 6))
task_list.append(Task('t3', x, Status.ready, 0, 5))

reso = {
    R1: 1,
    R2: 1,
    R3: 1}

FCFS_scheduler = Scheduler(reso, task_list, alogorithm_type=AlgoModel.FCFS)
FCFS_scheduler.start()
