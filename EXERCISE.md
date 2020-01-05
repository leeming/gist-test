# Github API

Write a script that uses the Github API to query a user’s publicly available gists. When the script is first run, it should display a listing of all the user’s publicly available gists. On subsequent runs the script should list any gists that have been published since the last run. The script may optionally provide other functionality (possibly via additional command line flags) but the above functionality must be implemented.

## Notes

Inputs:
- username

List users public gist
store timestamp of when last run

Assumptions:
- subsequent runs for a given user, therefore store map of (user,date)
- "published" => created, not updated