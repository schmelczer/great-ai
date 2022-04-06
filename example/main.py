import json
from random import shuffle

from devtools import debug
from predict_domain import predict_domain

from good_ai import process_batch, serve

if __name__ == "__main__":
    serve(predict_domain)
    
    with open(".cache/ss-data-0/s2-corpus-1583.json") as f:
        raw = json.load(f)

    shuffle(raw)
    data = {f'{r["title"]} {r["abstract"]}': r["domain"] for r in raw[:5]}

    results = process_batch(predict_domain, data.keys())

    for predicted, actual in zip(results, data.values()):
        print(", ".join(actual))
        debug(predicted)
        print()
