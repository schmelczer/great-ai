import json

from predict_domain import predict_domain

from good_ai import LargeFile, process_batch

if __name__ == "__main__":
    with open("data/s2-corpus-1583.json") as f:
        raw = json.load(f)

    LargeFile.configure_credentials_from_file("s3.ini")

    data = {f'{r["title"]} {r["abstract"]}': r["domain"] for r in raw[:5]}

    print(process_batch(predict_domain, ["We have found a new type of chemical."]))
