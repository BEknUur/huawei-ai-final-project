"""Statistics by meetings
How to run: PYTHONPATH=. python scripts/data_stats.py  ->  results/data_stats.csv
"""

import csv
from pathlib import Path

from diarization import get_regions, load_rttm, load_uem

DATA = Path("data")
COLUMNS = [
    "split",
    "meeting",
    "duration_h",
    "speech_h",
    "single_h",
    "overlap_h",
    "overlap_pct",
    "n_speakers",
]


def meeting_stats(meeting):
    ref = load_rttm(DATA / "ref_rttm" / f"{meeting}.rttm")[meeting]
    uem = load_uem(DATA / "uem" / f"{meeting}.uem")[meeting]
    regions = get_regions(ref, uem)

    duration = uem.duration()
    single = regions["single"].duration()
    overlap = regions["overlap"].duration()
    nonspeech = regions["nonspeech"].duration()
    assert abs(single + overlap + nonspeech - duration) < 1e-3, meeting

    return {
        "meeting": meeting,
        "duration": duration,
        "single": single,
        "overlap": overlap,
        "speakers": set(ref.labels()),
    }


def make_row(split, name, duration, single, overlap, speakers):
    speech = single + overlap
    return {
        "split": split,
        "meeting": name,
        "duration_h": round(duration / 3600, 3),
        "speech_h": round(speech / 3600, 3),
        "single_h": round(single / 3600, 3),
        "overlap_h": round(overlap / 3600, 3),
        "overlap_pct": round(100 * overlap / speech, 1),
        "n_speakers": len(speakers),
    }


def main():
    rows = []
    for split in ["dev", "test"]:
        meetings = (DATA / "splits" / f"{split}.txt").read_text().split()
        stats = [meeting_stats(m) for m in meetings]

        for s in stats:
            row = make_row(
                split,
                s["meeting"],
                s["duration"],
                s["single"],
                s["overlap"],
                s["speakers"],
            )
            if not 1 <= row["overlap_pct"] <= 50:
                print(f"WARNING {s['meeting']}: overlap {row['overlap_pct']}%")
            rows.append(row)

        rows.append(
            make_row(
                split,
                "TOTAL",
                sum(s["duration"] for s in stats),
                sum(s["single"] for s in stats),
                sum(s["overlap"] for s in stats),
                set().union(*(s["speakers"] for s in stats)),
            )
        )

    Path("results").mkdir(exist_ok=True)
    with open("results/data_stats.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
