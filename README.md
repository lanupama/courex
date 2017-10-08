This code uses the requests module

USAGE:

$ python2.7 github_user_search.py username passwd count
where count is no of users not exceeding 1000 which is the github limit

Please note, it will take a few small changes to run on python3.


TODO's

1) Not yet explored all of Python requests module eg : params feature
2) Not handled all server responses for now.
   In particular '403 forbidden' is a common error code for different reasons.
   So assuming it only for rate limit violation is not  correct. Also
   the tradeoffs between incurring an api-hit with rate limit violation and apriory
   checking the rate limit before issuing a search request must be carefully evaluated.
3) Timeout and incomplete results support needs to be added

