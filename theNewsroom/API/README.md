So, to have docker-compose automatically set up the postgres database for you, you need to do the following:

## Installing needed tools

If Mac/Windows
	1. Do the Docker Desktop install (if there is an option to include docker-compose in the download, say yes)

If Linux
	1. Install the Docker Engine (https://docs.docker.com/engine/install/#server)
	2. Then go here to install docker-compose (https://docs.docker.com/compose/install/)



## Starting docker-compose to run

1. Navigate to the 'API' directory
2. Execute the following command `docker-compose up`
	- It's gonna print some stuff out and hopefully the last line looks something like this
	'''
	postgresdb_1  | 2020-10-10 05:07:30.894 UTC [1] LOG:  database system is ready to accept connections
	'''
3. BOOM, ready to go. The postgres database is listening on port 5432 of your local machine.
4. to tear it down, do `docker-compose down` in the same directory.


## Entering into the postgres database

1. Execute the following command
	'''
	psql -h 127.0.0.1 -p 5432 -U postgres
	'''
- password is stored in the docker-compose file (all local so no security worries)
- I set it to 'password'

2. If you do `\dt newscollectorinfo.*` and no tables show up, do the following:
	- `\l` -> see that there is a database called newsroom_something...
	- execute `\c thenewsroom_database` 
		- By default, one connects to the 'postgres' database
		- We just need to switch 
3. After connecting to the right db, you should be able to do `\dt newscollectorinfo.*` to see the tables that I've set up to be pre-populated

NOTE: I've organised the first set of tables under a schema, so `\dt` doesn't work by itself. Idk why, but the fix is the include the schema.

Example query
```
SELECT * FROM newscollectorinfo.articleinfo;
```
