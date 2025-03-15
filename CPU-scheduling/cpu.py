import queue

def fcfs(processes):
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
    time, waiting_time, turnaround_time = 0, [], []
    gantt_chart = []
    
    for pid, at, bt in processes:
        if time < at:
            time = at
        waiting_time.append(time - at)
        gantt_chart.append((pid, time, time + bt))
        time += bt
        turnaround_time.append(time - at)
    
    avg_wt = sum(waiting_time) / len(processes)
    avg_tat = sum(turnaround_time) / len(processes)
    
    return gantt_chart, waiting_time, turnaround_time, avg_wt, avg_tat

def sjf(processes):
    processes.sort(key=lambda x: (x[1], x[2]))  # Sort by arrival time, then burst time
    time, waiting_time, turnaround_time = 0, [], []
    gantt_chart = []
    completed = []
    
    while len(completed) < len(processes):
        available = [p for p in processes if p not in completed and p[1] <= time]
        if not available:
            time += 1
            continue
        available.sort(key=lambda x: x[2])  # Sort by burst time
        pid, at, bt = available[0]
        waiting_time.append(time - at)
        gantt_chart.append((pid, time, time + bt))
        time += bt
        turnaround_time.append(time - at)
        completed.append(available[0])
    
    avg_wt = sum(waiting_time) / len(processes)
    avg_tat = sum(turnaround_time) / len(processes)
    
    return gantt_chart, waiting_time, turnaround_time, avg_wt, avg_tat

def srt(processes):
    remaining_time = {p[0]: p[2] for p in processes}  # PID -> Remaining burst time
    time, completed = 0, []
    waiting_time, turnaround_time = {}, {}
    gantt_chart = []
    
    while len(completed) < len(processes):
        available = [p for p in processes if p[1] <= time and p[0] not in completed]
        if not available:
            time += 1
            continue
        available.sort(key=lambda x: remaining_time[x[0]])
        pid, at, _ = available[0]
        gantt_chart.append((pid, time, time + 1))
        remaining_time[pid] -= 1
        if remaining_time[pid] == 0:
            completed.append(pid)
            turnaround_time[pid] = time + 1 - at
            waiting_time[pid] = turnaround_time[pid] - processes[[p[0] for p in processes].index(pid)][2]
        time += 1
    
    avg_wt = sum(waiting_time.values()) / len(processes)
    avg_tat = sum(turnaround_time.values()) / len(processes)
    
    return gantt_chart, list(waiting_time.values()), list(turnaround_time.values()), avg_wt, avg_tat

def round_robin(processes, quantum):
    queue = [p for p in sorted(processes, key=lambda x: x[1])]
    time, waiting_time, turnaround_time = 0, {}, {}
    gantt_chart = []
    remaining_time = {p[0]: p[2] for p in processes}
    
    while queue:
        pid, at, _ = queue.pop(0)
        if remaining_time[pid] > quantum:
            gantt_chart.append((pid, time, time + quantum))
            remaining_time[pid] -= quantum
            time += quantum
            queue.append((pid, at, remaining_time[pid]))
        else:
            gantt_chart.append((pid, time, time + remaining_time[pid]))
            time += remaining_time[pid]
            turnaround_time[pid] = time - at
            waiting_time[pid] = turnaround_time[pid] - processes[[p[0] for p in processes].index(pid)][2]
    
    avg_wt = sum(waiting_time.values()) / len(processes)
    avg_tat = sum(turnaround_time.values()) / len(processes)
    
    return gantt_chart, list(waiting_time.values()), list(turnaround_time.values()), avg_wt, avg_tat

def display_results(gantt_chart, waiting_time, turnaround_time, avg_wt, avg_tat):
    print("\nGantt Chart:")
    for pid, start, end in gantt_chart:
        print(f"{pid} ({start}-{end})", end=" → ")
    print("\n\nWaiting Times:", waiting_time)
    print("Turnaround Times:", turnaround_time)
    print(f"Average Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")

if __name__ == "__main__":
    while True:
        print("\nCPU Scheduling Simulator")
        print("1. First-Come, First-Served (FCFS)")
        print("2. Shortest-Job-First (SJF)")
        print("3. Shortest-Remaining-Time (SRT)")
        print("4. Round Robin (RR)")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "5":
            break
        
        n = int(input("Enter number of processes: "))
        processes = []
        for i in range(n):
            pid = f"P{i+1}"
            at = int(input(f"Enter arrival time of {pid}: "))
            bt = int(input(f"Enter burst time of {pid}: "))
            processes.append((pid, at, bt))
        
        if choice == "1":
            results = fcfs(processes)
        elif choice == "2":
            results = sjf(processes)
        elif choice == "3":
            results = srt(processes)
        elif choice == "4":
            quantum = int(input("Enter time quantum: "))
            results = round_robin(processes, quantum)
        else:
            print("Invalid choice. Try again.")
            continue
        
        display_results(*results)

