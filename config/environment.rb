# Load the rails application
require File.expand_path('../application', __FILE__)

# Location of dbaas-api
GenieDb::Application.config.DbaasApiEndpoint = 'http://localhost:8000/api/'

# Auth Token for dbaas-api
GenieDb::Application.config.DbaasApiToken = 'f156238116b83268e2ab4bcce16e771a412a6df7'

# Initialize the rails application
GenieDb::Application.initialize!
