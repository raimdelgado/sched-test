import math 
import random
import numpy as np
import sys

class RtTask:
    def_name = 'rt_task'

    def __init__(self,period,execution,priority,name = def_name,deadline = None):
        # task parameters
        self.name = name if name != "" else self.def_name
        self.period = int(period)

        self.deadline = int(period) if deadline == None or deadline == "" else int(deadline)
        self.execution = int(execution)

        if 0 < int(priority) < 100:
            self.priority = int(priority)
        else:
            print("Invalid priority: should be between 1 and 99")
            print("Will generate random priority...")
            self.priority = random.randint(1,99)
            print("Task priority is " + str(self.priority))

        # scheduling parameters
        self.cpu_util = 0
        self.wcrt = 0
        self.lub_issched = bool()
        self.rtt_issched = bool()
        self.entry = 0 # in case task has the same name and priority

        # runtime parameters
        self.curr_deadline  = 0
        self.isrun = False
        self.deadlines = [] # will be depracated 
        self.starttimes = []
        self.endtimes = []
        self.process_time = self.execution

    def get_cpu_util(self):
        self.cpu_util = self.execution / self.period 
        return self.cpu_util

    def get_deadlines(self, hyperperiod):
        curDeadline = self.deadline
        while curDeadline <= hyperperiod:
            self.deadlines.append(curDeadline)
            curDeadline += self.deadline

    def get_higher_priority_taskset(self, tasks):
        hp_tasks = []

        for task in tasks:
            if task.name == self.name and task.priority == self.priority:
                if task.entry == self.entry: 
                    continue
                else:
                    pass # in progress : when same priority and name
            
            if  task.priority > self.priority:
                hp_tasks.append(task)

        return hp_tasks

    def get_wcrt(self, tasks):
        hp_tasks = self.get_higher_priority_taskset(tasks)
        Ri, D = self.execution, self.deadline
        Ci, prevRi = Ri, 0
        while prevRi != Ri and D > prevRi:
            I, prevRi = 0, Ri
            for task in hp_tasks:
                I = I + math.ceil(Ri / task.period) * task.execution
            Ri = Ci + I
        self.wcrt = Ri
        return self.wcrt
    
    def update_curr_deadline(self, currentTime):
        while self.curr_deadline <= currentTime:
            self.curr_deadline += self.deadline


class RtTaskset:
    def __init__(self):
        self.tasks = []
        self.no_of_tasks = 0
        self.hyperperiod = 0
        self.total_cpu_util = 0.

    def add_rt_task(self, rttask):
        for task in self.tasks:
            if rttask.name == task.name and rttask.priority == task.priority:
                rttask.entry = task.entry + 1
        
        self.tasks.append(rttask)
        self.no_of_tasks += 1

    def del_rt_task(self, index):
        if self.is_empty() is True or index > self.no_of_tasks:
            print("Cannot delete tasks[" + str(index) + "]: Taskset is either empty or index > no_of_tasks!")
        else:
            self.tasks.pop(index)

    def del_all_tasks(self):
        if self.is_empty() is False:
            self.tasks.clear()
        else:
            print("Warning: There are no tasks to clear!")

    def is_empty(self):
        return True if self.no_of_tasks==0 else False

    def sort_by_prio(self):
        if self.is_empty() is False:
            self.tasks = sorted(self.tasks, reverse=True, key=lambda rt_task: rt_task.priority)
        else:
            print("Warning: There are no tasks to sort")

    def get_hyperperiod(self):
        if self.is_empty() is False:
            periods = [task.period for task in self.tasks]
            self.hyperperiod = np.lcm.reduce(periods)
            return self.hyperperiod

        else:
            print("Warning: There are no tasks to get hyperperiod")

    def is_harmonic(self):
        if self.is_empty() is False:
            for i in range(self.no_of_tasks):
                dividend = self.tasks[i].period
                for j in range(self.no_of_tasks):
                    divisor = self.tasks[j].period
                    if divisor == dividend or divisor > dividend:
                        continue
                    if dividend % divisor != 0:
                        return False
            return True
        else:
            print("Warning: There are no tasks to check harmonicity")

    def get_total_cpu_util(self):
        if self.is_empty() is False:
            self.total_cpu_util = sum([task.get_cpu_util() for task in self.tasks])
            return self.total_cpu_util
        else:
            print("Warning: There are no tasks to get total cpu utilization")

    def get_wcrts(self): # don't know if necessary
        if self.is_empty() is False:
            for task in self.tasks:
                task.get_wcrt(self.tasks)
        else:
            print("Warning: There are no tasks to get wcrt")

    def init_curr_deadlines(self):
        if self.is_empty() is False:
            for task in self.tasks:
                task.update_curr_deadline(0)
        else:
            print("Warning: There are no tasks to update curr deadlines")


def LUBTest(taskset):
    taskset.sort_by_prio()
    tmp_taskset = RtTaskset()
    is_sched = 0
    
    for task in taskset.tasks:
        tmp_taskset.add_rt_task(task)
        n = tmp_taskset.no_of_tasks
        lub = n * (2**(1/n)-1) # Liu and Leyland Bound
        task.lub_issched = True
        if tmp_taskset.get_total_cpu_util() > lub:
            task.lub_issched = False
    
    is_sched = True if taskset.get_total_cpu_util() <= lub else False 
    return (is_sched, lub)


def RTTest(taskset):
    taskset.sort_by_prio()
    tmp_taskset = RtTaskset()
    is_sched = 0
    
    for task in taskset.tasks:
        tmp_taskset.add_rt_task(task)
        task.get_wcrt(tmp_taskset.tasks) # results accessed through task.wcrt

        if task.wcrt > task.deadline:
            task.rtt_issched = False
            is_sched += 1
        else:
            task.rtt_issched = True   

    return True if is_sched == 0 else False    


### should be executed in another thread 
def PriorityBasedPreemptiveScheduler(taskset,hperiod_scale):
    taskset.sort_by_prio() # sort tasks by priority
    taskset.init_curr_deadlines() # get first deadlines
    hyperperiod = taskset.get_hyperperiod() * hperiod_scale # get hyperperiod

    lub_issched, lub = LUBTest(taskset)

    if lub_issched is False: # double check with RT test, whether the tasks are schedulable 
        print("LUB Test: Total utilization is greater than LUB - " + str(taskset.total_cpu_util) + " > " +str(lub))
        rtt_issched = RTTest(taskset)

    if lub_issched is False and rtt_issched is False: # the taskset is not schedulable
        sys.exit("LUB:" + str(lub_issched) + "RTTest:" + str(rtt_issched) + "Taskset is not schedulable!")
    else:
        CPU0 = [0] * hyperperiod 
        prev_task = RtTask(0,0,0)

        for i in range(hyperperiod):
            for task in taskset.tasks:
                if i == task.curr_deadline:
                    task.update_curr_deadline(i)
                    task.process_time = task.execution
           
            curr_task = getInstantHighestPriority(taskset)
            if curr_task is None:
                CPU0[i] = curr_task
            else:
                if curr_task.isrun == False:
                    curr_task.isrun = True
                    curr_task.starttimes.append(i)

                CPU0[i] = curr_task.name
                curr_task.process_time -= 1

                if curr_task.process_time == 0:
                    curr_task.isrun = False
                    curr_task.endtimes.append(i+1)
                
                if prev_task != curr_task and prev_task.process_time != 0:
                    prev_task.isrun = False
                    prev_task.endtimes.append(i)

                prev_task = curr_task
            # print(str(i+1) +" " +  str(CPU0[i]))

def getInstantHighestPriority(taskset):
    tmp_taskset = RtTaskset()
    for task in taskset.tasks:
        if task.process_time != 0:
            tmp_taskset.add_rt_task(task)

    if tmp_taskset.is_empty() is False:
        tmp_taskset.sort_by_prio()
        return(tmp_taskset.tasks[0])
    else:
        return None


# yes = RtTask(10,5,90,'t1')
# yes2 = RtTask(40,5,70,'t3')
# yes3 = RtTask(80,5,60,'t4')

# yesset = RtTaskset()
# yesset.add_rt_task(yes)
# yesset.add_rt_task(yes2)
# yesset.add_rt_task(yes3)

# print(LUBTest(yesset))
# print(yes.lub_issched)

