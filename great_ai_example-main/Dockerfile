FROM test

COPY requirements.txt .
RUN pip install --no-cache-dir ./great_ai

COPY mongo.ini .
COPY deploy.ipynb .

# RUN python3 -m large_file --backend s3 -secrets ~/.aws/credentials --cache my_first_file.json:3 my_second_file my_folder:0

CMD ["deploy.ipynb"]
