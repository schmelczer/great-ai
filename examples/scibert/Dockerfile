FROM schmelczera/great-ai:v0.1.4

COPY requirements.txt ./
RUN pip install --no-cache-dir --requirement requirements.txt

COPY . ./

RUN large-file --backend s3 --secrets s3.ini --cache scibert-highlights

CMD ["deploy.ipynb"]
