from dataclasses import dataclass
from enum import Enum


class Resource:
    def __init__(self, name: str):
        self.name = name


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
    tasks_order = ""

    def __init__(self, resource: dict[Resource, int], tasks_list: list[Task], algorithm_type: AlgoModel,
                 Quantum_for_RR: int = 5):
        self._resource = resource
        self._ready_Q: list[Task] = tasks_list
        self._waiting_Q: list[Task] = []
        self._current_time = 0
        self._Algorithm_type = algorithm_type
        self._quantum = Quantum_for_RR

    def __str__(self):
        output = ""
        output += f"time : {self._current_time} sec \n"
        for res, res_number in self._resource.items():
            output += f"{res.name}: {res_number}\t"

        output += f"\nRunning task : {self._running_task_name}\n"

        readyQ_task_str = "[ "
        waitingQ_task_str = "[ "
        for task in self._ready_Q:
            readyQ_task_str += task.name + " "
        for task in self._waiting_Q:
            waitingQ_task_str += task.name + " "

        output += f"ready queue: {readyQ_task_str}]\n"
        output += f"waiting queue: {waitingQ_task_str}]\n"

        return output

    def _add_to_readyQ(self, process):
        self._ready_Q.append(process)

    def _add_to_waitingQ(self, process):
        self._waiting_Q.append(process)

    def _assign_process_by_priority(self):
        self._ready_Q.sort(key=lambda task: task.task_type.priority, reverse=True)
        chosen_process: Task or None = self._ready_Q.pop()
        return chosen_process

    def _assign_process_by_first_come(self):
        chosen_process: Task or None = self._ready_Q.pop(0)
        return chosen_process

    def _assign_process_by_shortest_job_first(self):
        self._ready_Q.sort(key=lambda task: task.burst_time, reverse=True)
        chosen_process: Task = self._ready_Q.pop()
        return chosen_process

    def _assign_process_for_HRRN(self):
        self._ready_Q.sort(key=lambda task: ((self._current_time - task.burst_time) / task.burst_time))
        chosen_process: Task = self._ready_Q.pop()
        return chosen_process

    # todo : work on this method
    def _assign_process(self, algo_type=AlgoModel.FCFS):
        # Note : if you want to pick FCFS by priority use two below lines
        # if algo_type == AlgoModel.FCFS:
        #     return self._assign_process_by_priority()
        if algo_type == AlgoModel.FCFS:
            return self._assign_process_by_first_come()
        if algo_type == AlgoModel.RR:
            return self._assign_process_by_first_come()
        if algo_type == AlgoModel.SJF:
            return self._assign_process_by_shortest_job_first()
        if algo_type == AlgoModel.HRRN:
            return self._assign_process_for_HRRN()

    def _can_use_resources(self, task1: Task):
        satisfy = False
        for res in task1.task_type.resource_type:
            if self._resource[res] < 1:
                return satisfy

        satisfy = True
        for res in task1.task_type.resource_type:
            self._resource[res] -= 1

        return satisfy

    def _chose_task(self, algo_type):

        if len(self._ready_Q) == 0:
            print(self.tasks_order + "end\n")
            if len(self._waiting_Q) == 0:
                print("*********    tasks done succesfuly   **********")
                exit(0)
            else:
                print("_________________ deadlock accured __________________")
                exit(1)

        task = self._assign_process(algo_type)
        while not self._can_use_resources(task) and len(self._ready_Q) > 0:
            self._add_to_waitingQ(task)
            task = self._assign_process(algo_type)

        self._running_task_name = task.name
        return task

    def _run_FCFS(self, task: Task):
        for i in range(task.burst_time):
            print(self)
            self._current_time += 1
        print(self)

    def _free_resources(self, task: Task):
        for res in task.task_type.resource_type:
            self._resource[res] += 1

    def _update_queues(self):
        for task in self._waiting_Q:
            addable_to_ready_queue = True
            for res in task.task_type.resource_type:
                if self._resource[res] <= 0:
                    addable_to_ready_queue = False
                    break

            if addable_to_ready_queue:
                self._waiting_Q.remove(task)
                self._add_to_readyQ(task)
            else:
                task.task_type.priority += 1

    def _run_RR(self, task: Task):
        remainig_time = min(task.burst_time, self._quantum)
        for _ in range(remainig_time):
            print(self)
            self._current_time += 1
        print(self)
        task.burst_time -= remainig_time

        if task.burst_time != 0:
            self._ready_Q.append(task)

    def _run_SJF(self, task: Task):
        for _ in range(task.burst_time):
            print(self)
            self._current_time += 1
        print(self)

    def _run(self, algo_type):
        task = self._chose_task(algo_type)

        if algo_type == AlgoModel.FCFS:
            self._run_FCFS(task)

        if algo_type == AlgoModel.RR:
            self._run_RR(task)

        if algo_type == AlgoModel.SJF:
            self._run_SJF(task)

        if algo_type == AlgoModel.HRRN:
            self._run_FCFS(task)
        self.tasks_order += task.name + " => "
        self._free_resources(task)
        self._running_task_name = None
        self._update_queues()
        print("after resource free up : ________________")
        print(self)

    def start(self):
        if self._Algorithm_type == AlgoModel.RR or self._Algorithm_type == AlgoModel.FCFS:
            self._ready_Q.sort(key=lambda task: task.task_type.priority)
        else:
            self._ready_Q.sort(key=lambda task: task.task_type.priority, reverse=True)
        while True:
            self._run(self._Algorithm_type)


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

########################### test1 ---------------------------
# Note: this is a test
# task_list = [Task('t1', y, Status.ready, 0, 3),
#              Task('t2', x, Status.ready, 0, 6),
#              Task('t3', x, Status.ready, 0, 5)]
#
# reso = {
#     R1: 1,
#     R2: 1,
#     R3: 1}

###########################  test2 ----------------------------

task_list = [Task('t1', x, Status.ready, 0, 3),
             Task('t2', z, Status.ready, 0, 6),
             Task('t3', x, Status.ready, 0, 1),
             Task('t4', y, Status.ready, 0, 10),
             # Task('t5', y, Status.ready, 0, 5),
             # Task('t6', z, Status.ready, 0, 15)
             ]

reso = {
    R1: 2,
    R2: 2,
    R3: 2
}

# FCFS_scheduler = Scheduler(reso, task_list, algorithm_type=AlgoModel.FCFS)
# FCFS_scheduler.start()


# RR_scheduler = Scheduler(reso, task_list, algorithm_type=AlgoModel.RR, Quantum_for_RR=2)
# RR_scheduler.start()

# SJF = Scheduler(reso, task_list, algorithm_type=AlgoModel.SJF)
# SJF.start()

hrrn = Scheduler(reso, task_list, algorithm_type=AlgoModel.HRRN)
hrrn.start()
