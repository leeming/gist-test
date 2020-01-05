# equal-experts-gist
Gist scanner for Equal Experts tech test

## Usage

This tool only expects the main USERNAME argument. To search for public gists belonging to the user 'leeming', run the following

```
python src/public_gist/public_gists.py leeming
```

This will output a list of gists by the user with the following format: "[gist id] - [creation date] - [description]", e.g.

```
366777776e64e5fb4e9e085561d2d787 - 2020-01-04T14:23:58Z - another example
bbf842499d3a5273c36fdda876034ae7 - 2020-01-04T14:09:15Z - first example
```

To enable debugging you can pass the `-v ` (`--verbose`) flag:
```
python src/public_gist/public_gists.py -v leeming
```

Any subsequent lookups for the same user's gists will only return new gists created after previously running the tool.
State is tracked by default in the '.gist_last_queried' pickle file (Pickle is a python serialization library - https://docs.python.org/3/library/pickle.html). If you want to reset the state, simply remove this file. The tool could be extended in the future to support resetting user state via commandline arguments.


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