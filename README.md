## Description
The goal of this lab is to do resource allocation using both an optimistic resource manager and the banker’s algorithm of Dijkstra. The optimistic resource manager is simple: Satisfy a request if possible, if not make the task wait; when a release occurs, try to satisfy pending requests in a FIFO manner.

Your program takes one command line argument, the name of ﬁle containing the input. After reading (all) the input, the program performs two simulations: one with the optimistic manager and one with the banker. Output is written to stdout (the screen). Input ﬁles for thirteen required runs are available on the web, together with the expected output.

The input begins with two values T,the number of tasks,and R, the number of resource types,followed by R additional values,the number of units present of eachresource type. (If you set ‘‘arbitrary limits’’ on say T or R, you must, document this in your readme,checkthat the input satisﬁes the limits, print an error if it does not, and set the limits high enough so that the required inputs all pass.) Then come multiple inputs, each representing the next activity of a speciﬁc task. The possible activities are initiate, request, compute, release, and terminate. Time is measured in ﬁxed units called cycles and, for simplicity, no fractional cycles are used. The manager can process one activity (initiate, request, or release) for eachtask in one cycle. However,the terminate activity does NOT require a cycle.

To ease the programming,Ihavespeciﬁed all activities to have the same format, namely a string followed by three unsigned integers.

The initiate activity (which must precede all others for that task) is written:
```
initiate task-number resource-type initial-claim
```

(The optimistic manager ignores the claim.) If there are R resource types,there are R initiate activities for eachtask, eachrequiring one cycle.

The request and release activities are written:
```
request task-number resource-type number-requested 
release task-number resource-type number-released
```

The compute activity is written:
```
compute task-number number-of-cycles unused
```

This activity means that for the next several cycles the process is computing and will make no requests or releases.The process retains its current resources during the computation. The fourth value is not used; I include it so that all activities have the same format.

Finally the terminate operation, whichdoes NOT require a cycle is written:
```
terminate task-number unused unused
```

The last two values are not used; I include them so that all activities have the same format.

### Input
As in lab 1 (linker) we use free form input. Hence a single activity mayspan several lines and (parts of) several activities may be on one line.For lab 3 I advise you to read all the data before processing.The data for eachtask occurs in order,but the tasks themselves may be interspersed. Input set 1, on the web and reprinted below,has all of task one followed by all of task two.Input set 8, on the web,represents the same run but the lines for tasks one and two are interleaved.

### Running the program
Your program must read its input from a ﬁle,whose name is given as a command line argument. The format of the input is shown above.

### Output
At the end of the run, print, for eachtask, the time taken, the waiting time,and the percentage of time spent waiting.Also print the total time for all tasks,the total waiting time,and the overall percentage of time spent waiting.

### Error checks
When implementing banker’salgorithm, if a task’sinitial claim exceeds the resources present or if,during execution, a task’srequests exceed its claims,print an informative message,abort the task, and release all its resources.This does not apply to the optimistic allocator since it does not have the concept of initial claim.

### Deadlock
Deadlock cannot occur for banker’s algorithm, but can for the optimistic resource manager. If deadlock is detected, print a message and abort the lowest numbered deadlocked task after releasing all its resources. If deadlock remains, print another message and abort the next lowest numbered deadlocked task, etc.

We learned sophisticated algorithms for detecting deadlock. You are NOT expected to implement one of these. Instead you should use the following simple algorithm that detects a deadlock when all non-terminated tasks have outstanding requests that the manager cannot satisfy. Note that, if a deadlock actually occurs during cycle n, you maynot detect it until muchlater since there may be non-deadlocked processes running.Ifyou detect the deadlock at cycle k, you abort the task(s) at cycle k and hence its/their resources become available at cycle k+1. This simple deadlock detection algorithm is not used in practice.

### Important Note
Items returned at time n are not available until time n+1, For example, if task 1 returns 10 units during cycle 6-7 and task 3 requests 10 units during that same cycle,the 10 units returned by task 1 are not available for the optimistic manager to give out and, when the banker makes its safety check, these 10 units are not considered available.They become available at time 7 for use in cycle 7-8.

### First data set
The input for the ﬁrst run is:

```
2 1 4 
initiate 1 1 4 
request 1 1 1 
release 1 1 1 
terminate 1 0 0 
initiate 2 1 4 
request 2 1 1 
release 2 1 1 
terminate 2 0 0
```

The ﬁrst line asserts that this run has 2 tasks and 1 resource type with 4 units.

The next line indicates that the run begins (at cycle 0-1, the cycle starting at 0 and ending at 1) with task 1 claiming (all) 4 units of resource 1. Further down on line 6 we see that task 2 also claims 4 units of resource 1during cycle 0-1.

From lines 3 and 7 we learn that eachtask requests a unit during cycle 1-2 and returns that unit during the next cycle after the request is granted. Forthe optimistic manager,the request is granted at 2 (the end of cycle 1-2) and the resource is returned during 2-3.

Input 1 does not use the compute activity.For the optimistic manager eachtask terminates at time 3.
