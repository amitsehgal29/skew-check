# skew-check

Spot key skew in a CSV column before you join or partition on it. Standard-library Python only.

One hot key (say, a default `customer_id` of `0`) can make a single Spark task or partition run far longer than the rest. This reports the distinct key count, the top keys and their share of rows, the max-to-mean ratio, and any key above a share threshold.

```
python3 skew_check.py orders.csv customer_id --top 5 --threshold 0.2
```

Exits 1 when a hot key is found.

Run tests: `python3 -m unittest -v`
