import argparse
import sys
import logging
import datetime
import pickle
import requests


_logger = logging.getLogger(__name__)


GITHUB_API_URL = "https://api.github.com"
TIMESTAMP_DICT_FILE = ".gist_last_queried"

# Dict to track when users where queried the last. Username is the key, date is the value
user_timestamps = dict()


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Querys GitHub user's public gists")
    parser.add_argument(
        dest="user",
        help="GitHub user to look up",
        type=str,
        metavar="user")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="Enables debugging output",
        action="store_const",
        const=logging.DEBUG)
    return parser.parse_args(args)


def get_user_public_gist(user: str) -> str:
    # Check to see if this is the first time this user has been queried or not
    if user in user_timestamps.keys():
        _logger.debug("Only showing gists since last time user was queried")
        r = requests.get("{}/users/{}/gists?since={}".format(GITHUB_API_URL, user, user_timestamps[user]))
    else:
        _logger.debug("This is the first time the user has been queried so show all gists")
        r = requests.get("{}/users/{}/gists".format(GITHUB_API_URL, user))
    
    if r.status_code == 403:
        _logger.warning("Failed to fetch due to API limiting")
        raise LookupError("API limit reached")
    elif r.status_code != 200:
        _logger.warning("Failed to get gists")
        raise LookupError("API request failed")

    return r.json()

# Pretty print gists json to stdout
def list_gists(json: str) -> None:
    if len(json) == 0:
        print("No public gists for this user")
        return

    for gist in json:
        print("{} - {} - {}".format(gist['id'], gist['created_at'], gist['description']))

def get_timestamp() -> str:
    # Timezones are hard and github requires it this as Z is a special UTC designator
    return "{}Z".format(datetime.datetime.utcnow().isoformat())

def update_user_timestamp(user: str) -> None:
    global user_timestamps
    
    ts = get_timestamp()
    _logger.debug("Updating timestamp dict for {} with {}".format(user, ts))
    user_timestamps[user] = ts

def load_user_timestamps(file_path: str = TIMESTAMP_DICT_FILE) -> None:
    global user_timestamps

    _logger.debug("Loading userTimestamp data from file")
    _logger.debug("loading '{}'".format(file_path))
    
    try:
        tmp_dict = pickle.load(open(file_path, "rb")) 
        user_timestamps = dict()
        for user, date in tmp_dict.items():
            if valid_8601_date(date):
                user_timestamps[user] = date
            else:
                _logger.warning("Passed date '{}' is not valid ISO-8601, skipping".format(date))
        
        _logger.debug(user_timestamps)
    except FileNotFoundError:
        _logger.debug("Skipping due to no existing pickle file")

def valid_8601_date(date: str) -> bool:
    # No obvious built in lib to check for a valid date. Do a simple try catch.
    try:
        datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        return True
    except ValueError:
        return False

def store_user_timestamp(file_path: str = TIMESTAMP_DICT_FILE) -> None:
    _logger.debug("Storing userTimestamp data to file")
    _logger.debug(user_timestamps)
    pickle.dump(user_timestamps, open(file_path, "wb"))
    
def setup_logging(loglevel):
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")

def run(user: str) -> int:
    _logger.info("Getting public gists for '{}'".format(user))
    try:
        public_gist = get_user_public_gist(user)
        
        _logger.debug(public_gist)
        list_gists(public_gist)

        update_user_timestamp(user)
        store_user_timestamp()

        return len(public_gist)
    except LookupError:
        print("Failed to lookup user gists from Github")
        return 0


def main(args):
    args = parse_args(args)
    setup_logging(args.loglevel)
    load_user_timestamps()

    run(args.user)

if __name__ == "__main__":
    main(sys.argv[1:])
