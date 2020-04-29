% distrubuted real-time system representation:
% directed acyclic graph (DAG)
% % cap_gamma = {V,L} 
% where,
% V = {tau_1, ..., tau_n} % set of objects (tasks or messages)
% L -> directed edges representing communication flow

% Also, R = {r_1, ..., r_c} % set of resources supporting execution of
% objects

% Usually, assume mapping of objects to resources is fixed (not a part of
% decision variables

% An object, task or message is represented by:
% tau_i = {C_i, T_i, D_i, pi_i}
% where,
% C = worst-case execution
% T = period
% D = deadline
% pi = priority
% All are integers

%  Direct edge exist of tau_i writes to tau_j

