# bootstrap-moderator

A small script to add data to a running instance
of a [Moderator app](https://github.com/conversationai/conversationai-moderator). The data is in the CSV files in this repo.

To run, set two environment variables.

```shell
# The JWT authentication token generated for a Moderator service user
export MODERATOR_AUTH="JWT ..."

# The URL of the Moderator API
export MODERATOR_API=
```

You'll need to get a JWT auth token for a service user in your Moderator app. A "service" user has permission to use the publisher API to write and read data. To generate a JWT token for a service user, run the following command from the `/packages/cli` directory of the conversationai-moderator repo.
```
export TOKEN_SECRET={TOKEN_SECRET}
export TOKEN_ISSUER={TOKEN_ISSUER}
./bin/osmod.js users:get-token --id={USER_ID}
```
where `USER_ID` is the id of a Moderator user with type `service`.

Then run `python3 bootstrap_reviews.py` to load comments from each of the 3 data sets into Moderator. 
