# equal-experts-gist
Gist scanner for Equal Experts tech test

## Usage

This tool only expects the main USERNAME argument. To search for public gists belonging to the user 'ben', run the following

```
python src/public_gist/public_gists.py ben
```

This will output a list of gists by the user with the following format: "[gist id] - [creation date] - [description]", e.g.

```
b3e189a1579fe8c004d986565e233a85 - 2019-01-26T01:02:16Z - SCRIPT-8
52df4ee4d17a6c590a23f0a734cbe20e - 2016-05-27T16:06:03Z - Something like Hubot, implemented on top of Botkit
e54a1625ce7f3567edcc - 2015-11-20T04:25:38Z - After-hours switchover
10672053 - 2014-04-14T18:31:30Z - keybase.md
9568641 - 2014-03-15T15:02:50Z - None
6512874 - 2013-09-10T17:39:27Z - Libgit2 build results, before and after #1840
5484410 - 2013-04-29T20:14:13Z - https://github.com/libgit2/libgit2/issues/1508
4693571 - 2013-02-01T19:40:34Z - Clone example for http://ben.straub.cc/2013/02/01/stupid-libgit2-tricks-cloning/
4593102 - 2013-01-22T08:43:47Z - Resources from introductory class at PHP Benelux
4081592 - 2012-11-15T21:57:21Z - libgit2 summit notes
2144073 - 2012-03-21T03:37:09Z - Multi-cpu timing with libgit2 under MSVC
```

To enable debugging you can pass the `-v ` (`--verbose`) flag:
```
python src/public_gist/public_gists.py -v ben
```

Any subsequent lookups for the same user's gists will only return new gists published after previously running the tool.
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

To be able to run the test suite install the dev dependencies and run pytest
```
pip install -r requirements-dev.txt
pip install -e .
pytest tests/test_app.py
```