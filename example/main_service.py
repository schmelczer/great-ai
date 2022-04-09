import json
from random import shuffle

from devtools import debug
from predict_domain import predict_domain

from good_ai import process_batch, serve

if __name__ == "__main__":
    serve(predict_domain)
