# Train Domain classifier from the [semantic scholar dataset](https://api.semanticscholar.org/corpus)

## Upload the dataset (or a part of it) to shared infrastructure

```sh
mkdir ss-data && cd ss-data
wget https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/2022-02-01/manifest.txt
wget -B https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/2022-02-01/ -i manifest.txt
cd -
python3 -m great_ai.open_s3 --secrets s3.ini --push ss-data
rm -rf ss-data
```
