classdef rt_task < handle
    % creates a class for a real-time task
    properties
        name = 'rt task' % task name
        period % task period in desired unit
        deadline % task deadline
        computation % task computation time
        priority % task priority (between 0~99, where 99 is the highest)
        lub_issched
        rttest_issched
        wcrt
        run = struct('process_time',[],'deadlines', [],'start_times',[], 'end_times', [])
    end
    methods
        function obj=rt_task(name,Tp,Td,Tc,prio)
            % Constructor of the rt_task class. 
            % The arguments should be ordered as follows:
            %   name = name/identifier of the task
            %   Tp = task period
            %   Td = task deadline
            %   Tc = computation time / busy period
            %   prio = task priority (between 0~99, where 99 is the highest)
            % Make sure that Tp, Td, and Tc has the same unit.
            if nargin == 5 
                obj.name = name;
                obj.period = Tp;
                obj.deadline = Td;
                obj.computation = Tc;
                obj.run.process_time = obj.computation;
                
                if 0 < prio && prio < 100
                    obj.priority = prio;
                else
                    error('Error. \n priority must be between 0 and 99')
                end 
            end
        end
        function setLubSched(obj, lub)
            obj.lub_issched = lub;
        end
        function u = getUtilization(obj)
            u = obj.computation / obj.period;
        end
        function Ri = getWCRT(obj, tasks)
            % Calculates the worst case response time (WCRT) of the task
            % Ri is the WCRT and calculated as follows:
            % Ri = Wi + Ji
            %   Where, 
            %    J = jitter 
            %    W = busy period defined as:
            %    Wi  = Ci + Bi + Ii , and
            %    Ii = sigma_j( ceil(Wi + Jj / Pj) * Cj)
            %      Where,
            %       i = the current task
            %       j = taskset of tasks with higher priorities than ith task
            %       C = computation time
            %       B = blocking time (low priority preempts higher priority)
            %       I = interference time (high prioirty preempts higher ones)
            %       P = Period    
            % We assume that B = J = 0  
            % Thus, R = W, and can be simplified as:
            %   Ri = Ci + sigma_j(ceil(Ri/Pj) * Cj) 
            % This calculation should be iterated until Ri(x-1) == Ri(x),
            % or the loop should be broken when Ri(x) > D (deadline)

            checkRtTaskClass(tasks) % checks if the input is rt_task class

            % Create taskset for tasks with higher priority tasks
            [hp_tasks, j] = obj.getHigherPriorityTasks(tasks);
            
            %Compute response time
            Ri = obj.computation; 
            Ci = Ri; D = obj.deadline; 
            prevRi = 0; 
            while prevRi ~= Ri && D > prevRi
                I = 0; prevRi = Ri;
                for i =1:j
                    I = I + ceil(Ri / hp_tasks(i).period) * hp_tasks(i).computation;
                end
                Ri = Ci + I;
            end
            obj.wcrt = Ri;
        end
        function [hptasks, j] = getHigherPriorityTasks(obj, tasks)
            checkRtTaskClass(tasks) % checks if the input is rt_task class
            
            % Create taskset for tasks with higher priority tasks
            j = 0; 
            no_of_task = length(tasks);
            hp_tasks = rt_task;
            for i = 1:no_of_task 
                if tasks(i).name == string(obj.name)
                    continue
                end
                if tasks(i).priority > obj.priority
                    j = j+1;
                    hp_tasks(j) = tasks(i);
                end
            end
            hptasks = hp_tasks;
        end
        function deadlines = getDeadlines(obj, hyperperiod)
            i = 1;
            deadlines(i) = obj.deadline;
            while hyperperiod > deadlines
                deadlines(i+1) = deadlines(i)+ obj.deadline;
                i = i+1;
            end
            obj.run.deadlines = deadlines;
        end
        function checkRtTaskClass(task)
            % Check whether the input is of the class rt_task
            if isa(task,'rt_task') == 0
                error('Error. \n The input should be rt_task not %s', class(task))
            end
        end
    end
end
