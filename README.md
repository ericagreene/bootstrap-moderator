# bootstrap-moderator

A small script to add Amazon product review data to a running instance
of a [Moderator app](https://github.com/conversationai/conversationai-moderator). The data is a subset of publicly available data that you can find at
http://snap.stanford.edu/data/amazon/productGraph/.

To run, set two environment variables.

```shell
# The JWT authentication token generated for a Moderator service user
export MODERATOR_AUTH="JWT ..."

# The URL of the Moderator API
export MODERATOR_API=
```

Then run `python bootstrap_revies.py` with Python v3 to load 100 product reviews from each of the 3 data sets.
