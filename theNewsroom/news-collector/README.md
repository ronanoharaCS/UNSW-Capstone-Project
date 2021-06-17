This directory is responsible for collecting data from news API 
and inserting this data into the postgreSQL database: thenewsroom_database

# SET UP VIRTUAL ENV #

1. navigate to the capstone-project-comp3900-w17a-212-monolith/theNewsroom/news-collector/ directory
2. Create virtual environment called 'newscollector_env': 

	$ python3 -m venv newscollector_env

3. Activate the python virtual environment from this directory: (deactivating it is just $ deactivate) 
	
	$ source newscollector_env/bin/activate 

4. Install dependencies for the virtual environment:
	
	$ pip install -r requirements.txt

	# NOTE if you are on mac and it can't download psycopg2, do this
	```
	pip install psycopg2-binary
	```

5. Add git ignore, so the virtual environment dependencies aren't tracked by git:

	$ echo 'newscollector_env' > .gitignore

# COLLECT DATA #

1. Activate virtual env (as above): 
 
	$ source newscollector_env/bin/activate

2. Run the python script: 

	$ python collect_news.py

~ once you've collected data, you need to update thenewsroom_database file (theNewsRoom/API/postgres_db/init/03-Guardian_Data) that is loaded when running docker-compose up ~

3. To update this file, just run: 

	$ ./update_db 

	- and enter the database password: 'password'


