from pythonPackages.Giveme5W1H.Updator import Giveme5W1HUpdator
import logging
import geopy

# Do this cause we have to, otherwise, it won't work
geopy.geocoders.options.default_user_agent = "newsroom-application"

# Set up logger
logging.basicConfig(filename="GiveMe5WUpdator.log", level=logging.ERROR)

updator = Giveme5W1HUpdator()
updator.summariseArticles()
# need to add functions to analyse content and push it through the graphql 
