# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 12:19:41 2018

@author: Kenrick Tse
"""
import sys
import copy

# for a given state, returns true if it is safe, or false if not
def simulate(state):
    manager = state.pop(0)
    # just a list of how many of each resource the banker holds
    resources = manager[2:2+manager[1]] 
    
    processes = state
    
    # trivial case
    if (len(processes) <= 0):
        return True
    
    while(len(processes) > 0):
        none_valid = True

        # check each process to see if any of them have a max add'l
        # that is <= resources held by manager
        for i, process in enumerate(processes):
            valid = True
            for r in range(manager[1]): # for each resource
                if process[(r+1)*3] > resources[r]:
                    valid = False
            
            # if process max request can be met, add that process's resources
            # back to the manager and remove the process
            if valid:
                none_valid = False
                for r in range(manager[1]):
                    resources[r] += process[(r*3) + 2]
                processes.pop(i)
                
        if none_valid == True:
            return False
    
    return True
                    
        
    
if __name__ == '__main__':
    
    #########################################
    # setup and input cleaning
    #########################################
    
    with open(sys.argv[1], 'r') as input_file:
        raw = input_file.readlines()
        
    for i,l in enumerate(raw):
        if len(l) <= 1:
            del raw[i]
            
    data = raw.pop(0)
    data = data.split()
    # state[0] represents the number of tasks in the system, # resource types and
    # the amount of  each resource type held by manager. subsequent arrays in state
    # represent the n-th process and their resources (more detail below)
    state = [[int(data[0]), int(data[1])]]
        
    state += [[0] * (3 * int(data[1]) + 1) for i in range(int(data[0]))]
    for i in range(state[0][1]):
        state[0].append(int(data[2+i]))
    
    # cleaning the input
    for i, entry in enumerate(raw):
        raw[i] = raw[i].split()
        for j,k in enumerate(raw[i]):
            if j != 0:
                raw[i][j] = int(raw[i][j])
    
    raw2 = copy.deepcopy(raw) #raw2 is a deepcopy used to run the optimistic simulation
    state2 = copy.deepcopy(state) #state2 is a deepcopy used to run the optimistic simulation
    
    # the state 2D array contains all the information relevant to calculation.
    # after state[0], each subsequent array represents a process[n] in this format:
    # process[0] = current cycle of process.
    # process[1] = claim, process[2] = has resource 1, process[3] = max add resource 1, 
    # then mod 3 for each subsequent resource   
    
    #########################################
    # main program for banker's
    #########################################
    
    curr_cycle = 0
    end_cycle = [0] * state[0][0] # used to store end cycle of each process
    wait_count = [0] * state[0][0] # used to count total # waiting cycles of each process
    curr_wait = [0] * state[0][0] # used to count cycles since last non-block of each process
    
    # order of checking activities for processes. processes blocked longest have priority.
    # any processes that were blocked are removed from the order list and appended to the block
    # list, and the order of processing for subsequent cycles prioritizes tasks that were blocked.
    order = [i+1 for i in range(state[0][0])] 
    block_list = []
    active_processes = state2[0][0]
    # every iteration of the outer loop represents a cycle.
    while len(raw) >= 1:
        # indicates amount of each resource released by 'release' instruction. resets with each cycle.
        to_release = [0] * state[0][1]
        new_order = copy.deepcopy(order)
        for curr_process in order:
            for i, entry in enumerate(raw):
                task = entry[1]

                if state[task][0] == curr_cycle:      
                    
                    if entry[0] == 'initiate' and entry[1] == curr_process and state[task][0] == curr_cycle:
                        resource = entry[2] - 1 # -1 for 0 indexing
                        state[task][0] += 1 # update cycle
                        
                        # error check if initial claim > total available resources
                        if(entry[3] > state[0][entry[2] + 1]):         
                            print(f'Aborting task {curr_process} for making initial claim exceeding # units present')
                            # set all values of process to 0
                            for j, val in enumerate(state[curr_process]):
                                state[curr_process][j] = 0
                            state[curr_process][0] = -2 # -2 signifies abort, as opposed to -1 for termination
                            
                            # delete remaining activities pertaining to aborted task
                            raw = [entry for entry in raw if not entry[1] == curr_process]
                            if(curr_process in block_list):    
                                block_list.pop(block_list.index(i))
                            if(curr_process in new_order):
                                new_order.pop(new_order.index(curr_process))
                            end_cycle[task-1] = -2 
                            active_processes -= 1
                            
                        # if error check passed
                        else:
                            # set claim and max add of the indicated process and 0 for has
                            state[task][resource * 3 + 1] = entry[3] # claim = claim
                            state[task][(resource * 3) + 3] = entry[3] # max add'l = claim
                            state[task][(resource * 3) + 2] = 0 # has = 0 at start
                            
                            del raw[i]

                        
                    elif entry[0] == 'release' and entry[1] == curr_process and state[task][0] == curr_cycle:
                        
                        resource = entry[2] - 1
                        to_release[resource] += entry[3]
                        state[task][(resource * 3) + 2] -= entry[3] # update amt of resource held
                        state[task][(resource * 3) + 3] += entry[3] # update max add'l
                        
                        state[task][0] += 1 # update cycle
                        del raw[i]

                        
                    elif entry[0] == 'compute' and entry[1] == curr_process and state[task][0] == curr_cycle:
                        state[task][0] += entry[2] # add the specified quantity to cycle
                        del raw[i]

                        
                    elif entry[0] == 'request' and entry[1] == curr_process and state[task][0] == curr_cycle:
                        state[task][0] += 1 # update cycle
                        resource = entry[2] - 1
                        
                        # error check if request exceeds initial claim
                        if(state[task][(resource * 3) + 2] + entry[3] > state[task][(resource * 3) + 1]):
                            print(f'Aborting task {curr_process} for exceeding initial claim on resource {resource+1}\n')
                            # relinquish outstanding resources
                            for j, resource in enumerate(to_release):
                                to_release[j] += state[curr_process][(j*3)+2]
                                
                            # set all values of process to 0
                            for j, val in enumerate(state[curr_process]):
                                state[curr_process][j] = 0
                            state[curr_process][0] = -2 # -2 signifies abort, as opposed to -1 for termination
                            
                            # delete remaining activities pertaining to aborted task
                            raw = [entry for entry in raw if not entry[1] == curr_process]
                            if(curr_process in block_list):    
                                block_list.pop(block_list.index(i))
                            if(curr_process in new_order):
                                new_order.pop(new_order.index(curr_process))
                            end_cycle[task-1] = -2 
                            active_processes -= 1
                        
                        # error check passed                            
                        else:
                            new_state = copy.deepcopy(state)
                            new_state[0][resource + 2] -= entry[3] # subtract requested amt from manager
                            new_state[task][(resource * 3) + 2] += entry[3] # add requested amt
                            new_state[task][(resource * 3) + 3] -= entry[3] # subtract from max add'l
                            
                            # run bankers to see if new state that incorporates request is safe
                            result = simulate(copy.deepcopy(new_state))
        
                            if result == True:
                                state = new_state
                                curr_wait[task-1] = 0
                                if(curr_process in block_list):
                                    block_list.pop(block_list.index(curr_process))
                                    
                                if(curr_process not in new_order):
                                    new_order.append(curr_process)
                                del raw[i]
                            else:
                                wait_count[task-1] += 1 # request was blocked, increment wait counter
                                curr_wait[task-1] += 1
                                
                                # prioritize tasks that have been blocked longest
                                # add to back of list of blocked tasks if not already in list
                                if(curr_process not in block_list):
                                    block_list.append(curr_process)
                                # remove from list of unblocked tasks if needed
                                if(curr_process in new_order):
                                    new_order.pop(new_order.index(curr_process))
                            
                    elif entry[0] == 'terminate' and entry[1] == curr_process and state[task][0] == curr_cycle:
                        # record ending cycle of process
                        end_cycle[task-1] = state[task][0] 
                        
                        if(curr_process in new_order):
                            new_order.pop(new_order.index(curr_process))
                        if(curr_process in block_list):    
                                block_list.pop(block_list.index(i))
                        # relinquish outstanding resources
                        for j, resource in enumerate(to_release):
                            to_release[j] += state[task][(j*3)+2]
                            
                        # set all values of process to 0
                        for j, val in enumerate(state[task]):
                            state[task][j] = 0
                        state[task][0] = -1
                        active_processes -= 1
                        del raw[i]

                else: continue

        # add released resources back to manager for next cycle
        curr_cycle += 1
        for i, resource in enumerate(to_release):
            state[0][2 + i] += resource
        
        # update order for next cycle, prioritizing things that were blocked
        order = block_list + new_order
            
    
    #############################################
    # main program for optimistic algorithm
    #############################################
    
    curr_cycle = 0
    end_cycle2 = [0] * state2[0][0] # used to store end cycle of each process
    wait_count2 = [0] * state2[0][0] # used to count total # waiting cycles of each process
    block_list = []
    order = [i+1 for i in range(state2[0][0])] 
    active_processes = state2[0][0]

    while len(raw2) >= 1:
        # indicates amount of each resource released by 'release' instruction. resets with each cycle.
        to_release = [0] * state2[0][1]
        new_order = copy.deepcopy(order)
        
        for curr_process in order:
            for i, entry in enumerate(raw2):
                task = entry[1]
                if state2[task][0] == curr_cycle:      
                    
                    if entry[0] == 'initiate' and entry[1] == curr_process and state2[task][0] == curr_cycle:
                        resource = entry[2] - 1 # -1 for 0 indexing
                        
                        # set claim and max add of the indicated process and 0 for has
                        state2[task][resource * 3 + 1] = entry[3] # claim = claim
                        state2[task][(resource * 3) + 3] = entry[3] # max add'l = claim
                        state2[task][(resource * 3) + 2] = 0 # has = 0 at start
                        
                        state2[task][0] += 1 # update cycle
                        del raw2[i]

                        
                    elif entry[0] == 'release' and entry[1] == curr_process and state2[task][0] == curr_cycle:
                        
                        resource = entry[2] - 1
                        to_release[resource] += entry[3]
                        state2[task][(resource * 3) + 2] -= entry[3] # update has amt
                        state2[task][(resource * 3) + 3] += entry[3] # update max add'l
                        
                        state2[task][0] += 1 # update cycle
                        del raw2[i]
 
                        
                    elif entry[0] == 'compute' and entry[1] == curr_process and state2[task][0] == curr_cycle:
                        state2[task][0] += entry[2] # add the specified quantity to cycle
                        del raw2[i]

                        
                    elif entry[0] == 'request' and entry[1] == curr_process and state2[task][0] == curr_cycle:
                        state2[task][0] += 1 # update cycle
                        resource = entry[2] - 1
                        
                        # so long as the manager has enough of requested resource, grant request
                        if(state2[0][resource + 2] - entry[3] >= 0):
                            state2[0][resource + 2] -= entry[3] # subtract requested amt from manager
                            state2[task][(resource * 3) + 2] += entry[3] # add requested amt
                            state2[task][(resource * 3) + 3] -= entry[3] # subtract from max add'l (not technically necessary)
                            
                            if(curr_process in block_list):
                                block_list.pop(block_list.index(curr_process))
                                new_order.append(curr_process)
                            del raw2[i]
                        else:
                            # prioritize tasks that have been blocked longest
                            # add to back of list of blocked tasks if not already in list
                            if(curr_process not in block_list):
                                block_list.append(curr_process)
                            # remove from list of unblocked tasks if needed
                            if(curr_process in new_order):
                                new_order.pop(new_order.index(curr_process))
                            wait_count2[task-1] += 1

                    elif entry[0] == 'terminate' and entry[1] == curr_process and state2[task][0] == curr_cycle:
                        # record ending cycle of process
                        end_cycle2[task-1] = curr_cycle 
                        
                        # relinquish outstanding resources
                        for j, resource in enumerate(to_release):
                            to_release[j] += state2[task][(j*3)+2]
                            
                        # set all values of process to 0
                        for j, val in enumerate(state2[task]):
                            state2[task][j] = 0
                        state2[task][0] = -1
                        active_processes -= 1
                        del raw2[i]

                else: continue
        # if all processes blocked, abort first process and release its resources
        if(active_processes == len(block_list)):
            for i, process in enumerate(state2):
                if i != 0 and process[0] > -1:
                    # relinquish outstanding resources
                    for j, resource in enumerate(to_release):
                        to_release[j] += state2[i][(j*3)+2]
                        
                    # set all values of process to 0
                    for j, val in enumerate(state2[i]):
                        state2[i][j] = 0
                    state2[i][0] = -2 # -2 signifies abort, as opposed to -1 for termination
                    
                    # delete remaining activities pertaining to aborted task
                    raw2 = [entry for entry in raw2 if not entry[1] == i]
                    block_list.pop(block_list.index(i))
                    end_cycle2[i-1] = -2 
                    break
            active_processes -= 1

                            
        # add released resources back to manager for next cycle
        curr_cycle += 1
        for i, resource in enumerate(to_release):
            state2[0][2 + i] += resource
        
        # base case to account for off by one errors in aborting tasks
        if(len(raw2) == 1):
            if raw2[0][0] == 'terminate':
                if(end_cycle2.count(-2) > 1):
                    end_cycle2[raw2[0][1] - 1] = curr_cycle - 1
                    wait_count2[raw2[0][1] -1] -= 1
                else:
                    end_cycle2[raw2[0][1] - 1] = curr_cycle
                state2[raw2[0][1]][0] = -1
                raw2.pop()
        # update order for next cycle, prioritizing things that were blocked
        order = block_list + new_order
        
        
    ####################################
    # printing output
    ####################################
    
    print('FIFO\n==========')
    fifo_end_sum = 0
    fifo_wait_sum = 0
    for i, task in enumerate(end_cycle2):
        if end_cycle2[i] == -2:
            print(f'Task {i+1}\taborted')
        else:
            print(f'Task {i+1}\t{end_cycle2[i]}   {wait_count2[i]}   {int((wait_count2[i]/end_cycle2[i])*100)}%')
            fifo_end_sum += end_cycle2[i]
            fifo_wait_sum += wait_count2[i]
    print(f'Total\t{fifo_end_sum}   {fifo_wait_sum}   {int((fifo_wait_sum/fifo_end_sum)* 100)}%')
    
    
    print('\n\nBANKER\'S\n==========')
    bank_end_sum = 0
    bank_wait_sum = 0
    for i, task in enumerate(end_cycle):
        if end_cycle[i] == -2:
            print(f'Task {i+1}\taborted')
        else:
            print(f'Task {i+1}\t{end_cycle[i]}   {wait_count[i]}   {int((wait_count[i]/end_cycle[i])*100)}%')
            bank_end_sum += end_cycle[i]
            bank_wait_sum += wait_count[i]
    print(f'Total\t{bank_end_sum}   {bank_wait_sum}   {int((bank_wait_sum/bank_end_sum)*100)}%')
