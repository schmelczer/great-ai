# Train a domain classifier on the [semantic scholar dataset](https://api.semanticscholar.org/corpus)

![steps](diagrams/scope.svg)

## Install

### System dependencies

Make sure you have `python3`, `pip`, and `venv` installed.
> On Ubuntu, execute: `sudo apt install -y python3 python3-pip python3-venv`

### Install dependencies
```sh
python3 -m venv --copies .env 
source .env/bin/activate

pip install -r requirements.txt
```
## Execute 

- [Part 1](src/data.ipynb)
- [Part 2](src/train.ipynb)
- [Part 3](src/deploy.ipynb)
