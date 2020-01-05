import pytest
from src.public_gist import public_gists
import json
import os

@pytest.fixture
def empty_json ():
    return json.dumps(dict())

@pytest.mark.parametrize('user', ["", "foobarfoobarfoobarfoobarfoobar"])
def test_github_bad_user(user):
    with pytest.raises(LookupError):
        public_gists.get_user_public_gist(user)

def test_public_gist_no_history():
    public_gists.user_timestamps=dict()
    assert len(public_gists.get_user_public_gist("leeming")) == 2

@pytest.mark.parametrize('date, expected', [("2020-12-12T00:00:00Z",0),("2020-01-04T14:20:00Z",1),("",2)])
def test_public_gist_with_history(date, expected):
    public_gists.user_timestamps={'leeming':date}
    assert len(public_gists.get_user_public_gist("leeming")) == expected

def test_load_time_both_empty(tmpdir):
    #Store empty dict
    public_gists.user_timestamps=dict()
    public_gists.store_user_timestamp(str(tmpdir.join("test_load_time_both_empty.p")))

    # Set dict to be a temp value that should be overwritten
    public_gists.user_timestamps={'foo':'bar'}
    
    # Load in empty dict
    public_gists.load_user_timestamps(str(tmpdir.join("test_load_time_both_empty.p")))

    assert public_gists.user_timestamps == dict()

def test_load_time_bad_pickle(tmpdir):
    #Store empty dict
    public_gists.user_timestamps={'foo':'bar'}    
    public_gists.store_user_timestamp(str(tmpdir.join("test_load_time_bad_pickle.p")))
    public_gists.load_user_timestamps(str(tmpdir.join("test_load_time_bad_pickle.p")))

    assert public_gists.user_timestamps == dict()

def test_load_time_good_pickle(tmpdir):
    #Store empty dict
    public_gists.user_timestamps={'leeming':'2020-12-12T00:00:00.00000Z'}    
    public_gists.store_user_timestamp(str(tmpdir.join("test_load_time_good_pickle.p")))
    public_gists.load_user_timestamps(str(tmpdir.join("test_load_time_good_pickle.p")))

    assert public_gists.user_timestamps == {'leeming':'2020-12-12T00:00:00.00000Z'}

def test_e2e_user_gist_history_stored(tmpdir):
    public_gists.TIMESTAMP_DICT_FILE=str(tmpdir.join("e2e.p"))

    # Make sure state is empty
    public_gists.user_timestamps=dict()
    public_gists.store_user_timestamp()

    assert public_gists.run("leeming") == 2
    assert public_gists.run("leeming") == 0