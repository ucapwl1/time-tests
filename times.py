import datetime

_FMT = "%Y-%m-%d %H:%M:%S"


def time_range(start_time, end_time, number_of_intervals=1, gap_between_intervals_s=0):
    start_time_s = datetime.datetime.strptime(start_time, _FMT)
    end_time_s = datetime.datetime.strptime(end_time, _FMT)

    # Basic validations
    if end_time_s <= start_time_s:
        raise ValueError("end_time must be after start_time")
    if number_of_intervals < 1:
        raise ValueError("number_of_intervals must be >= 1")
    if gap_between_intervals_s < 0:
        raise ValueError("gap_between_intervals_s must be >= 0")

    total_s = (end_time_s - start_time_s).total_seconds()
    # Each interval length so that n intervals + (n-1) gaps fill [start, end]
    d = (total_s - gap_between_intervals_s * (number_of_intervals - 1)) / number_of_intervals
    if d <= 0:
        raise ValueError("Intervals and gaps do not fit within the given time window")

    # Build ranges (keep return type as strings for compatibility)
    sec_range = []
    for i in range(number_of_intervals):
        a = start_time_s + datetime.timedelta(seconds=i * (d + gap_between_intervals_s))
        b = a + datetime.timedelta(seconds=d)
        sec_range.append((a.strftime(_FMT), b.strftime(_FMT)))
    return sec_range


def compute_overlap_time(range1, range2):
    overlap_time = []
    for start1, end1 in range1:
        for start2, end2 in range2:
            low = max(start1, start2)
            high = min(end1, end2)
            if low < high:  # keep only real (non-empty) overlaps
                overlap_time.append((low, high))
    return overlap_time


if __name__ == "__main__":
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    print(compute_overlap_time(large, short))