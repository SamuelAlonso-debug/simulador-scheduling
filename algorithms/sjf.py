from models.process import GanttEntry

def sjf(queue, current_time):
    if not queue:
        return None, current_time

    # Elegir el proceso con menor tiempo restante
    process = min(queue, key=lambda p: p.remaining_time)
    queue.remove(process)

    start = max(current_time, process.arrival_time)
    end = start + process.remaining_time

    process.remaining_time = 0

    return GanttEntry(process.pid, start, end), end