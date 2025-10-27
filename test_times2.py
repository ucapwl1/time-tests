# test_times.py
import pytest
from times import time_range, compute_overlap_time

@pytest.mark.parametrize(
    ("time_range_1", "time_range_2", "expected"),
    [
        # 1) generic case from the brief (two 7-minute chunks with a 1-min gap)
        (
            time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00"),
            time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", number_of_intervals=2, gap_between_intervals_s=60),
            [
                ("2010-01-12 10:30:00", "2010-01-12 10:37:00"),
                ("2010-01-12 10:38:00", "2010-01-12 10:45:00"),
            ],
        ),
        # 2) no overlap at all
        (
            time_range("2010-01-12 10:00:00", "2010-01-12 10:10:00"),
            time_range("2010-01-12 10:20:00", "2010-01-12 10:30:00"),
            [],
        ),
        # 3) touching endpoints (end == start) → empty overlap by convention
        (
            time_range("2010-01-12 10:00:00", "2010-01-12 10:10:00"),
            time_range("2010-01-12 10:10:00", "2010-01-12 10:20:00"),
            [],
        ),
        # 4) several intervals on both sides (no gaps)
        (
            time_range("2010-01-12 10:00:00", "2010-01-12 10:40:00", number_of_intervals=2, gap_between_intervals_s=0),
            time_range("2010-01-12 10:10:00", "2010-01-12 10:50:00", number_of_intervals=2, gap_between_intervals_s=0),
            [
                ("2010-01-12 10:10:00", "2010-01-12 10:20:00"),
                ("2010-01-12 10:20:00", "2010-01-12 10:30:00"),
                ("2010-01-12 10:30:00", "2010-01-12 10:40:00"),
            ],
        ),
    ],
)
def test_overlaps(time_range_1, time_range_2, expected):
    assert compute_overlap_time(time_range_1, time_range_2) == expected


def test_time_range_backwards_raises():
    # keep the negative test separate and explicit
    with pytest.raises(ValueError, match=r"end_time must be after start_time"):
        time_range("2010-01-12 12:00:00", "2010-01-12 10:00:00")
