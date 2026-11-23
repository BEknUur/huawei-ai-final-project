"""Diarization scoring per region.

Rules: collar = 0, skip_overlap = False, one speaker mapping per meeting.
"""


def map_hypothesis(ref, hyp, uem):
    """Rename hypothesis speakers using one optimal mapping for the whole meeting."""
    raise NotImplementedError()


def score_meeting(ref, hyp, uem):
    """Seconds of missed / false alarm / confusion / total for each region."""
    raise NotImplementedError()
