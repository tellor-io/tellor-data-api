# Tellor Data API
Backfill and store Tellor on-chain events into a PostgreSQL database. Includes a REST API for accessing the data using HTTP requests.

# Objectives
* Store the Tellor smart contract event data in a local (postgreSQL) database
* Create a REST API for accessing events data


# Usage Guide
This projects requires that you rescan the Ethereum blockchain to _backfill_ the data for Tellor since it was launched in August 2019.

Begin by creating a `docker-compose.yml` file from the sample the run:
```
docker-compose up
```
After 20 seconds database will attempt to backfill and you'll see messages like:
```
webserver_1  | Difference between last and current block too large
webserver_1  | Taking incremental step from 8307471 to 8307721
webserver_1  | Scanning and saving events from 8307471 to 8307721
webserver_1  | Found Events:  27
```
Appear in the logs. The backfill will continue to run but you can now use the _API endpoints_.

You can change the `BLOCK_RANGE_MAX` to `1000` blocks during the backfill process.

After the backfill, there is a recurring HTTP GET request made to the webserver to keep in sync with the events on chain. The update interval can be changed using the `POLL_INTERVAL` variable.

# API Documentation
The following endpoints are of the form `/api/event` where `event` is a Tellor smart contract event. Each endpoint returns the 100 most recent events.
```
/api/newDispute
/api/voted
/api/disputeVoteTallied
/api/newTellorAddress
/api/newStake
/api/stakeWithdrawn
/api/stakeWithdrawnRequested
/api/approval
/api/transfer
/api/tipAdded
/api/dataRequested
/api/newChallenge
/api/newRequestOnDeck
/api/newValue
/api/nonceSubmitted
```
