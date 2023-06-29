from dataclasses import dataclass


# Note : define the Resources data class (struct)
@dataclass
class Resource:
    number: int


R1 = Resource(0)
R2 = Resource(0)
R3 = Resource(0)


# Note : define the type of tasks and then initial them
@dataclass
class Task_type:
    priority: int
    resource_type: list[Resource]


x = Task_type(3, [R1, R2])
y = Task_type(2, [R2, R3])
z = Task_type(1, [R1, R3])
