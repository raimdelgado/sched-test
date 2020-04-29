clear all; clc; close all;
%% Taskset
% Task attributes --> to table in GUI
% Schedulability
% task_names = {'\tau_1' '\tau_2'}; 
% task_periods = [10, 20];
% task_deadlines = task_periods; % assume that deadlines and periods are equal
% task_comps = [3, 5];
% task_prios = [99,80];

% Preemption
task_names = {'\tau_1' '\tau_2' '\tau_3'}; 
task_periods = [10, 20, 40];
task_deadlines = task_periods; % assume that deadlines and periods are equal
task_comps = [3, 5, 10];
task_prios = [99,80, 50];

if length(task_names) == length(task_periods) && length(task_periods) ...
        == length(task_deadlines) && length(task_deadlines) ...
    == length(task_comps) && length(task_comps) == length(task_prios)
    
    n_tasks = length(task_names);
else
    error('Error. \n Missing task attribute')
end

% create taskset from the attributes
taskset(1:n_tasks) = rt_task(); % preallocating for speed
for i = 1:n_tasks
    taskset(i) = rt_task(task_names(i),task_periods(i),task_deadlines(i), ...
        task_comps(i), task_prios(i));
end; clear i;


%% Periodic Tasks 
% scaleFactor = 10;
% [is_scaled,taskset] = scaleComputation(taskset,scaleFactor);

taskset = sortTaskPriority(taskset); % sort task according to priority
% check if the taskset has harmonic periods
% 1 if task periods are harmonic 
is_harmonic = isHarmonic(taskset); 
% is_harmonic

% calculate hyperperiod
hyperperiod = getHyperPeriod(taskset);

% Least Upper Bound (LUB) test 
% is_sched is 1 if schedulable
[lub_is_sched, lub, total_u] = LUBTest(taskset);
total_u

% response time (RT) test 
% is_sched is 1 if schedulable
rttest_is_sched = RTTest(taskset);

TaskReport(taskset);

%% Scheduler (Priority-based Preemptive Scheduler for Periodic Tasks)
% taskset = sortTaskPriority(taskset); % sort task according to priority
% TaskReport(taskset);
hyperperiod_scale =1 * hyperperiod;

CPU0 = zeros(hyperperiod_scale,1);
for i = 1:n_tasks
    taskset(i).getDeadlines(hyperperiod_scale);
end

k = ones(n_tasks,1);
currentDeadline = 0;
isRun = zeros(n_tasks,1);
prevj = 1;

for i = 1:hyperperiod_scale
    for j = 1:n_tasks
        wait_time = 0;

        currentDeadline = taskset(j).run.deadlines(k(j));
        if i > currentDeadline && k(j) <= length(taskset(j).run.deadlines) 
            k(j) = k(j) + 1;
            currentDeadline = taskset(j).run.deadlines(k(j));
            taskset(j).run.process_time = taskset(j).computation;
        end
        
        [hp_tasks, l] = taskset(j).getHigherPriorityTasks(taskset);
        for m = 1:l
            wait_time = wait_time + hp_tasks(m).run.process_time;
        end
        
        if wait_time == 0 && taskset(j).run.process_time > 0 %&& i <= currentDeadline
            if isRun(j) == 0
                isRun(j) = 1;
                taskset(j).run.start_times = [taskset(j).run.start_times i-1]; 
            end
            
            CPU0(i) = j;
            taskset(j).run.process_time = taskset(j).run.process_time - 1;
            
            if taskset(j).run.process_time == 0 
                isRun(j) = 0;
                taskset(j).run.end_times = [taskset(j).run.end_times i];
            end
            
            if j ~= prevj && taskset(prevj).run.process_time ~= 0
                isRun(prevj) = 0;
                taskset(prevj).run.end_times = [taskset(prevj).run.end_times i-1];
            end
            
            prevj = j;
            break;
        end
    end
end

%% Timeline
for i = 1:n_tasks
    lineNames{i} = string(taskset(i).name);
    startTimes{i} = taskset(i).run.start_times;
    endTimes{i} = taskset(i).run.end_times;
end
if rttest_is_sched == 1
    timelines(lineNames,startTimes,endTimes);
end
%% Functions
function [isScaled, newTaskset] = scaleComputation(tasks, scalingFactor)
    checkRtTaskClass(tasks) %check whether the input is rt_task class
    no_of_tasks = length(tasks);

    isScaled = 0;
    for i = 1:no_of_tasks
        if mod(tasks(i).computation, 1) ~= 0
            tasks(i).computation = tasks(i).computation * scalingFactor;
            tasks(i).period = tasks(i).period * scalingFactor;
            tasks(i).deadline = tasks(i).deadline * scalingFactor;
            isScaled = 1;
        end
    end
    newTaskset = tasks;
end


function hp_taskset = sortTaskPriority(tasks)

    checkRtTaskClass(tasks) %check whether the input is rt_task class
    
    no_of_tasks = length(tasks);
    for i = 1:no_of_tasks
        for j = 1:no_of_tasks-i
            if tasks(j).priority < tasks(j+1).priority
                temp = tasks(j);
                tasks(j) = tasks(j+1);
                tasks(j+1) = temp;
            end
        end
    end
    hp_taskset = tasks;
end

function y  = isHarmonic(tasks)
    % Checks if all periods in the taskset is harmonic,
    % if each period is an integer multiple of shorter periods.
    % Returns 1 if the taskset has harmonic periods, otherwise 0.
    checkRtTaskClass(tasks) %check whether the input is rt_task class
    
    no_of_tasks =length(tasks);
    y = 1;
    for i = 1:no_of_tasks
        dividend = tasks(i).period;
        for j = 1:no_of_tasks
            divisor = tasks(j).period;
            if divisor == dividend || divisor > dividend
                continue
            end
            if mod(dividend, divisor) ~= 0 
                y = 0;
                break
            end
        end
    end
    if y == 0, txt = ' not '; else, txt = ' '; end;
    fprintf('The task periods are%sharmonic!\n', txt)
end

function y = getHyperPeriod(tasks)
    % Returns the hyperperiod for a taskset
    % A set of periodic task repeats every hyperperiod
    % If the taskset is schedulable in one hyperperiod, it is schedulable
    % all the time, given there are no aperiodic or sporadic tasks, and no
    % resource constraints
    checkRtTaskClass(tasks) %check whether the input is rt_task class
    
    no_of_tasks = length(tasks);
    y = tasks(1).period;
    for i = 1:no_of_tasks
        y = getLCM(y, tasks(i).period); 
    end
end

function sigmaU = getTotalUtilization(tasks)
    % Returns the total CPU utilization of all tasks in the taskset
    % Input should be rt_task class
    checkRtTaskClass(tasks) %check whether the input is rt_task class
    
    no_of_tasks =length(tasks);
    sigmaU = 0;
    for i = 1:no_of_tasks
        sigmaU = sigmaU + tasks(i).getUtilization; 
    end
end

function [isSched, lub, sigmaU] = LUBTest(tasks)
    % Determines whehter a taskset is schedulable through 
    % the least-upper(utilization) bound (LUB) test
    % Returns a tuple [isSched, LUB, sigmaU]
    % Where, 
    %   isSched is 1 if the taskset is schedulable, 0 otherwise
    %   lub is the calculated least-upper bound , and
    %   sigmaU is the calculated total CPU utilzation of the taskset
    % Least-upper bound a.k.a. Liu and Leyland bound states that a taskset
    % is schedulable if the CPU utilization of all tasks are less than the 
    % calculated least-upper bound, or :
    %   sigmaU of n tasks (total CPU utilization) <= n(2^(1/n)-1)
    %   where n is the no_of_tasks
    checkRtTaskClass(tasks) %check whether the input is rt_task class

    no_of_tasks = length(tasks); isSched = 0;
    lub = no_of_tasks*(2^(1/no_of_tasks)-1); % calculate LUB
    sigmaU = getTotalUtilization(tasks);
    
    if sigmaU <= lub
        isSched = 1;

    end
end

function [isSched, tasks] = RTTest(tasks)
    % Checks the schedulability of a taskset using response time test
    % isSched is 1 if the taskset is schedulable, 0 otherwise
    checkRtTaskClass(tasks) %check whether the input is rt_task class
    
    no_of_tasks = length(tasks); isSched = 1;    
    for i = 1:no_of_tasks
        for j = 1:i
            tmpTaskSet(j) = tasks(j);
        end
        [lub_issched, lub, total_u] = LUBTest(tmpTaskSet);
        R = tasks(i).getWCRT(tmpTaskSet);     
        tasks(i).lub_issched = lub_issched;
        
        if lub_issched ~= 1
            D = tasks(i).deadline;
            if R > D
                isSched = 0;
            end
        end
        tasks(i).rttest_issched = isSched;
    end
end

function TaskReport(tasks)

    checkRtTaskClass(tasks) %check whether the input is rt_task class
    
    no_of_tasks = length(tasks);
    
    report_header = {'Task Name', 'Period', 'Deadline', 'Computation '...
        'LUB Test','RT Test', 'WCRT'};
    report = cell(no_of_tasks+1,7);
    report(1,:) = report_header;
    not_schedulable = 0;
    for i = 1:no_of_tasks
        
        report(i+1,1) = tasks(i).name;
        report(i+1,2) = num2cell(tasks(i).period);
        report(i+1,3) = num2cell(tasks(i).deadline);
        report(i+1,4) = num2cell(tasks(i).computation);
        report(i+1,5) = num2cell(tasks(i).lub_issched);
        report(i+1,6) = num2cell(tasks(i).rttest_issched);
        report(i+1,7) = num2cell(tasks(i).wcrt);
        if tasks(i).rttest_issched == 0
            not_schedulable = not_schedulable+1;
        end
    end
    display(report)
    if not_schedulable > 0, txt = ' not '; else, txt = ' '; end;
    fprintf('The taskset is%sschedulable!\n', txt)
    
end

function checkRtTaskClass(task)
    % Check whether the input is of the class rt_task
    if isa(task,'rt_task') == 0
        error('Error. \n The input should be rt_task not %s', class(task))
    end
end

function y = getLCM(A, B) 
    % Returns the least common multiple (LCM) of two numbers
    % You can just use lcm(A,B) function of Matlab
    % This is created for easier transition to other languages without LCM
    % function such as C/C++
    tmp = A;
    while 1
        if mod(tmp,B) == 0 && mod(tmp,A) == 0
            break
        end
        tmp = tmp+1;
    end
    y = tmp;
end