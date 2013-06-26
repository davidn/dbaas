# Load the rails application
require File.expand_path('../application', __FILE__)

# Location of dbaas-api
GenieDb::Application.config.DbaasApiEndpoint = 'http://localhost:8000/api/'

# Auth Token for dbaas-api
GenieDb::Application.config.DbaasApiToken = '291adc1a7726403cf8850abae7ca1d2d54c97321'

# Initialize the rails application
GenieDb::Application.initialize!
