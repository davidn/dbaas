class DeploymentRegion < ActiveRecord::Base
   attr_accessible :name
   attr_accessible :region_name
   
   ## ASSOCIATIONS ##
	 has_and_belongs_to_many :db_instances
   
end
