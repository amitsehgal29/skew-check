#!/usr/bin/env python3
"""Spot key skew in a CSV column before you join or partition on it.

Reports distinct keys, the top keys with their share of rows, the
max-to-mean ratio, and flags hot keys above a share threshold.
"""
import argparse, csv, json, sys
from collections import Counter

def skew(rows, column, top=5, threshold=0.2):
    counts = Counter()
    total = 0
    for r in rows:
        if column not in r:
            raise KeyError(f"column not found: {column}")
        counts[r[column]] += 1
        total += 1
    if not total:
        return {"rows": 0, "distinct": 0, "top": [], "max_to_mean": 0, "hot_keys": []}
    mean = total / len(counts)
    top_keys = [{"key": k, "rows": c, "share": round(c / total, 4)} for k, c in counts.most_common(top)]
    hot = [k for k, c in counts.most_common() if c / total > threshold]
    return {
        "rows": total, "distinct": len(counts), "top": top_keys,
        "max_to_mean": round(counts.most_common(1)[0][1] / mean, 2),
        "hot_keys": hot,
    }

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("path")
    p.add_argument("column")
    p.add_argument("--top", type=int, default=5)
    p.add_argument("--threshold", type=float, default=0.2, help="share of rows that makes a key hot")
    a = p.parse_args(argv)
    with open(a.path, newline="", encoding="utf-8") as fh:
        res = skew(csv.DictReader(fh), a.column, a.top, a.threshold)
    print(json.dumps(res, indent=2))
    return 1 if res["hot_keys"] else 0

if __name__ == "__main__":
    sys.exit(main())
