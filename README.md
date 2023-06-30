# implementation 
at first, we will determine the objects that they hold a meaningful idea from the project for example
<br>
- Task
- Resources
- Task_type(X,Y,Z)
- Status(ready, running, waiting)
- AlgoModel(FCFS, RR, SJF, HRRN)

and then we will implement Scheduler class to schedule the order of processes 
<br>
then we have the main idea of the Scheduling in ___run()__ method like below :

```python

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

        self._free_resources(task)
        self._running_task_name = None
        self._update_queues()
        print("after resource free up : ________________")
        print(self)
```

in this code we will give a task by the given algorithm that can be any of FCFC , RR, SJF or HRRN algorithms 
and then by the priority we want in each algorithm we will extract a __Task__ 
<br>
and then we will run them by the algorithm we want
and then in the __run-somthing()__ methods we will print the status in each time unit 
<br>
and then when we call `free_resources()` we will free the resources we don't need anymore
<br>
then we will make the `runnig_task` into __None__ and then, we will update the ready Queue and waiting Queue
<br>
and after that we will print the status that we are in it