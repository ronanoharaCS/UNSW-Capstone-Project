# README
Our team successfully developed a web application that aggregates articles from news APIs, and applies topic modelling to give the user a clear picture of the news landscape and trends.

# Software Stack
Javascript, Vue.js, Vuetify, Python, Postgresql, graphQL, node.js and docker

# UNSW-Capstone-Project
COMP3900 group: w17a-212-monolith

# CREATED BY
Lance Young
Ronan O’Hara
Liam Dale
Jonathan Chan
James Tatham

# Project
The Newsroom

# SETUP  

1. See INSTALL.md for installion instruction for the operating systems WINDOWS 10 / LINUX (UBUNTU) / MAC OSX

2. Install git-lfs
    ## Windows (WSL2) / Linux  
    `sudo apt install` 
    `sudo apt install git lfs`
    
    ## MAC OSX 
    `brew install git-lfs`
    `brew upgrade git-lfs`  
    
4. `git clone ttps://github.com/unsw-cse-capstone-project/capstone-project-comp3900-w17a-212-monolith.git`
    Note: you made need to do git pull after installing git-lfs 

6. Two termials are required for this step. One for running the database and one for running the front end.

## First teminal, Starting docker-compose to run
1. cd into the project folder. 
2. `cd /theNewsroom/API`
3. Execute the following command `sudo docker-compose up` on Linux/Windows 
or on Mac OSX just use `docker-compose up`

(to tear it down, do `docker-compose down` in the same directory.)

## Then start a second terminal
1. cd into the project folder. 
2. `cd /theNewsroom/front-end-client`
3. `npm install`
4. PORT=3000 npm run dev

To [see](see) the website now visit address localhost:3000 in a browser.


