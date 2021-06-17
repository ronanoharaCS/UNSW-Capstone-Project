# UNSW-Capstone-Project

# README

# COMP3900 group
comp3900-w17a-212-monolith

# CREATED BY
Lance Young
Ronan O’Hara
Liam Dale
Jonathan Chan
James Tatham

# Project
The Newsroom

# Sumission 
* Note: Our project exceeded the 100MB limit for submitting by zip file. We are instead submitting by the alternative Github method. 
* The final submission is on our branch "submission". The branch can be found at https://github.com/unsw-cse-capstone-project/capstone-project-comp3900-w17a-212-monolith/tree/submission
* This submission branch was last updated before 11:59pm on the 16/11/2020.

# If you need any help, please contact 
James Tatham - z5168119@unsw.edu.au - 0458732989

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


