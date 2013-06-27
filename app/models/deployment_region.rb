class DeploymentRegion < ActiveRecord::Base
   attr_accessible :name
   attr_accessible :region_name
   
   ## ASSOCIATIONS ##
   has_many :region_instances
   has_many :db_instances, :through => :region_instances
   
end
