def fcfs(processes):
    # sort processes dictionary based on arrival 
    processes = sorted(processes, key=lambda p:p['arrival'] )
    
    current_time = 0
    gantt_chart = []
    finish_time = {}
    waiting_time = {}
    turn_around_time = {}
    total_cpu_burst_time = 0

    for process in processes:
        procces_name = process['name']
        arival_time = process['arrival']
        burst_time = process['burst']

        start_time = max(current_time,arival_time)
        end_time = start_time + burst_time

        gantt_chart.append((procces_name,start_time,end_time))

        finish_time[procces_name] = end_time
        waiting_time[procces_name] = start_time - arival_time
        turn_around_time[procces_name] = end_time - arival_time

        current_time = end_time
        total_cpu_burst_time += burst_time
    
    total_time = gantt_chart[-1][2]
    cpu_utilization = round((total_cpu_burst_time / total_time) * 100, 2)

    total_waiting_time = 0
    for value in waiting_time.values():
        total_waiting_time += value
        
    avg_waiting_time = round(total_waiting_time / len(waiting_time), 2)

    total_turn_around_time = 0
    for value in turn_around_time.values():
        total_turn_around_time += value
    
    avg_tot = round(total_turn_around_time / len(turn_around_time), 2)
    
    print("\n--- FCFS Scheduling ---")
    print('Gantt Chart =', gantt_chart)
    print('Finish Time =', finish_time)
    print('Watinig Time =', waiting_time)
    print('Turnaround Time =', turn_around_time)
    print('Avarage Waiting Time = ' , avg_waiting_time)
    print('Average Turnaround Time =', avg_tot)
    print('CPU Utilization = %', cpu_utilization)

def srtf(processes):
    processes = sorted(processes, key=lambda p:p['arrival'] )
    n = len(processes)

    current_time = 0
    completed = 0
    remaining_burst = {}
    for process in processes:
        remaining_burst[process['name']] = process['burst']
    finish_time = {}
    waiting_time = {}
    turnaround_time = {}
    gantt_chart = []
    total_burst_time = 0
    for process in processes:
        total_burst_time += process['burst']
    executed_process = None
    
    # main loop, finish when all processes ends
    while completed < n:
        ready_queue = []
        # add processes to ready queue based on arrival and if the have remaning time
        for process in processes:
            if process['arrival'] <= current_time and remaining_burst[process['name']] > 0:
                ready_queue.append(process)
                
        if ready_queue:
            # sort based on shortest remaining time first
            ready_queue.sort(key=lambda p: remaining_burst[p['name']])  
            # current process is the process wiht shortest remainig time
            current_process = ready_queue[0] 
            process_name = current_process['name']

            # if its a new process in the gantt chart, record the start time
            if executed_process != process_name:
                if executed_process is not None:  # end the previous process segment
                    gantt_chart[-1] = (gantt_chart[-1][0], gantt_chart[-1][1], current_time)
                gantt_chart.append((process_name, current_time, None)) # we dont know when the process ends
                executed_process = process_name

            # execute the current process for one unit of time
            remaining_burst[process_name] -= 1
            current_time += 1

            # if the process finishe, record its finish time
            if remaining_burst[process_name] == 0:
                finish_time[process_name] = current_time
                completed += 1
        else:
            # if no process is ready, CPU is idle
            current_time += 1

    # add end time for the last process
    gantt_chart[-1] = (gantt_chart[-1][0], gantt_chart[-1][1], current_time)

    total_waiting_time = 0
    total_turnaround_time = 0

    for process in processes:
        process_name = process['name']
        turnaround_time[process_name] = finish_time[process_name] - process['arrival']
        waiting_time[process_name] = turnaround_time[process_name] - process['burst']
        total_waiting_time += waiting_time[process_name]
        total_turnaround_time += turnaround_time[process_name]

    avg_waiting_time = round(total_waiting_time / n, 2)
    avg_tot = round(total_turnaround_time / n, 2)

    total_time = gantt_chart[-1][2]
    cpu_utilization = round((total_burst_time / total_time) * 100, 2)
    
    print("\n--- SRTF Scheduling ---")
    print('Gantt Chart =', gantt_chart)
    print('Finish Time =', finish_time)
    print('Watinig Time =', waiting_time)
    print('Turnaround Time =', turnaround_time)
    print('Avarage Waiting Time = ' , avg_waiting_time)
    print('Average Turnaround Time =', avg_tot)
    print('CPU Utilization = %', cpu_utilization)

def round_robin(processes, quantum):
    current_time = 0 
    
    waiting_time = {}
    turnaround_time = {}
    remaining_burst = {}
    finish_time = {}

    for process in processes:
        waiting_time[process['name']] = 0  # set all waiting times to 0
        turnaround_time[process['name']] = 0  # set all turnaround times to 0
        remaining_burst[process['name']] = process['burst']  # copy burst time for each process

    ready_queue = []  
    gantt_chart = []  

    total_burst_time = sum(process['burst'] for process in processes) 
    
    # if any values of all processes its remaining time is more than 0 it well return true
    # and the loop will work until all remaining time for all processes is 0
    while any(remaining_burst[p['name']] > 0 for p in processes):
        # add new processes to the ready queue based on arrival time
        for process in processes:
            if process['arrival'] <= current_time and process not in ready_queue and remaining_burst[process['name']] > 0:
                ready_queue.append(process)

        # if the ready queue is empty, increase time and skip current loop until process come
        if not ready_queue:
            current_time += 1
            continue

        # get the next process from the ready queue
        current_process = ready_queue.pop(0)
        process_name = current_process['name']

        # execute the process for a time slice (quantum) or until it complete
        execution_time = min(quantum, remaining_burst[process_name])
        gantt_chart.append((process_name, current_time, current_time + execution_time))
        current_time += execution_time
        remaining_burst[process_name] -= execution_time

        # update waiting time for other processes in the ready queue
        for process in ready_queue:
            if remaining_burst[process['name']] > 0:
                waiting_time[process['name']] += execution_time

        # if the process hasent finished add it back to the ready queue
        if remaining_burst[process_name] > 0:
            ready_queue.append(current_process)
        else:
            # calculate finish time and tot for completed process
            finish_time[process_name] = current_time
            turnaround_time[process_name] = current_time - current_process['arrival']

    total_waiting_time = sum(waiting_time.values())
    total_turnaround_time = sum(turnaround_time.values())
    avg_waiting_time = round(total_waiting_time / len(processes),2)
    avg_turnaround_time = round(total_turnaround_time / len(processes),2)

    cpu_utilization = round((total_burst_time / current_time) * 100, 2)

    print("\n--- Round Robin Scheduling ---")
    print("Gantt Chart:", gantt_chart)
    print("Finish Time:", finish_time)
    print("Waiting Time:", waiting_time)
    print("Turnaround Time:", turnaround_time)
    print("Average Waiting Time:", avg_waiting_time)
    print("Average Turnaround Time:", avg_turnaround_time)
    print('CPU Utilization = %', cpu_utilization)

def read_processes(filename):
    # read processes in a text file and store it in dictionary
    processes = []
    quantum = 0

    with open(filename, 'r') as file:
        for line in file:
            # if a line start with Q it will the value into quantum
            if line.startswith("Q:"):  
                quantum = int(line.split(':')[1].strip())

            # read line and store process information in dictionary
            else:
                process_info = line.split()
                process = {
                    'name' : process_info[0],
                    'arrival' : int(process_info[1]),
                    'burst' : int(process_info[2])
                }
                
                processes.append(process)
    
    return quantum,processes

def main():
    filename = 'processes.txt'
    q,processes = read_processes(filename)
    fcfs(processes)
    srtf(processes)
    round_robin(processes,q)

if __name__ == "__main__":
    main()