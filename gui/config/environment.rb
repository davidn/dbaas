# Load the rails application
require File.expand_path('../application', __FILE__)

# Location of dbaas-api
GenieDb::Application.config.DbaasApiEndpoint = 'http://localhost:8000/api/'

# Auth Token for dbaas-api
GenieDb::Application.config.DbaasApiToken = '94c828a98f71e6f46b6e01ac71b0f4c1a31ff33b'

# Initialize the rails application
GenieDb::Application.initialize!
