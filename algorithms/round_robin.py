from models.process import GanttEntry

def round_robin(queue, quantum, current_time):
    if not queue:
        return None, current_time

    process = queue.pop(0)

    start = max(current_time, process.arrival_time)
    exec_time = min(quantum, process.remaining_time)
    end = start + exec_time

    process.remaining_time -= exec_time

    if process.remaining_time > 0:
        queue.append(process)

    return GanttEntry(process.pid, start, end), end