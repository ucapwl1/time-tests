# times.py
import datetime

_FMT = "%Y-%m-%d %H:%M:%S"

def time_range(start_time, end_time, number_of_intervals=1, gap_between_intervals_s=0):
    start_time_s = datetime.datetime.strptime(start_time, _FMT)
    end_time_s = datetime.datetime.strptime(end_time, _FMT)

    # keep your backwards-range validation from the previous step
    if end_time_s <= start_time_s:
        raise ValueError("end_time must be after start_time")

    d = (end_time_s - start_time_s).total_seconds() / number_of_intervals \
        + gap_between_intervals_s * (1 / number_of_intervals - 1)

    sec_range = [
        (start_time_s + datetime.timedelta(seconds=i * d + i * gap_between_intervals_s),
         start_time_s + datetime.timedelta(seconds=(i + 1) * d + i * gap_between_intervals_s))
        for i in range(number_of_intervals)
    ]
    return [(a.strftime(_FMT), b.strftime(_FMT)) for a, b in sec_range]

def compute_overlap_time(range1, range2):
    overlap_time = []
    for start1, end1 in range1:
        for start2, end2 in range2:
            low = max(start1, start2)
            high = min(end1, end2)
            if low < high:                 # <-- minimal fix
                overlap_time.append((low, high))
    return overlap_time
