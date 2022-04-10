import json
from random import shuffle

from devtools import debug
from predict_domain import predict_domain

from good_ai import process_batch

if __name__ == "__main__":
    with open(".cache/data-1/s2-corpus-323.json") as f:
        raw = json.load(f)

    shuffle(raw)
    data = {f'{r["title"]} {r["abstract"]}': r["domain"] for r in raw[:10]}

    results = process_batch(predict_domain, data.keys())

    for predicted, actual in zip(results, data.values()):
        print(", ".join(actual))
        debug(predicted)
        print()
