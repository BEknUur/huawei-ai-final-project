from collections import defaultdict

from pyannote.core import Annotation, Segment, Timeline


def load_rttm(path):
    """RTTM -> {meeting_id: Annotation}."""
    anns = defaultdict(Annotation)
    with open(path) as f:
        for line in f:
            p = line.split()
            if p and p[0] == "SPEAKER":
                start, dur = float(p[3]), float(p[4])
                anns[p[1]][Segment(start, start + dur)] = p[7]
    return dict(anns)


def load_uem(path):
    """UEM -> {meeting_id: Timeline}."""
    segs = defaultdict(list)
    with open(path) as f:
        for line in f:
            uri, _, s, e = line.split()
            segs[uri].append(Segment(float(s), float(e)))
    return {uri: Timeline(v).support() for uri, v in segs.items()}