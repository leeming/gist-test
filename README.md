# equal-experts-gist
Gist scanner for Equal Experts tech test

## Usage

## Prerequisites

### Virtualenv
It is assumed virtualenv is installed on the host

Create a virtualenv and activate it, e.g. on a Debian/Ubunutu based os do the following:
```
virtualenv -p /usr/bin/python3 venv

source venv/bin/activate
```

Install dependencies
```
pip install -r requirements.txt
```

To be able to run the test suite install the dev dependencies
```
pip install -r requirements-dev.txt
```

pip install -e .