from models.process import GanttEntry

def fcfs(queue, current_time):
    if not queue:
        return None, current_time

    process = queue.pop(0)

    start = max(current_time, process.arrival_time)
    end = start + process.remaining_time

    process.remaining_time = 0

    return GanttEntry(process.pid, start, end), end