class DeploymentRegion < ActiveRecord::Base
   attr_accessible :name
   
   ## ASSOCIATIONS ##
   has_many :db_instances
   
end
