This directory is responsible for creating an LDA topic model
and using this model to assign topics to articles in thenewsroom_database

~ The following steps assume you have already ran 'docker-compose up' in /theNewsroom/API ~

# SETUP VIRTUAL ENVIRONMENT #
 (only need to do this once) 

1. Create a virtual environment 
	
	$ python3 -m venv topic_analysis_env

2. Activate the virtual environment from this directory

	$ source topic_analysis_env/bin/activate 

3. Install dependencies for the virtual environment:
	
	$ pip install -r requirements.txt

4. Add git ignore, so the virtual environment dependencies aren't tracked by git:

	$ echo 'topic_analysis_env' > .gitignore

# CREATE LDA TOPIC MODEL #
(consider executing optimum_number_of_topics.py to determine an appropriate number of topics)

1. Activate the virtual environment 

	$ source topic_analysis_env/bin/activate

2. Create the LDA topic model based on the articles in thenewsroom_database

	$ python create_lda_model.py

3. Follow the prompts and visualise the database

4. If happy with the model, go manually assign topic names in update_topics_table.py

# ASSIGN TOPICS TO ARTICLES #

1. Update topics in the thenewsroom_database (newscollectorinfo.Topics table)

	$ python update_topics_table.py

2. Assign topics to each article

	$ python assign_article_topics.py























