class RegionInstances < ActiveRecord::Base
  attr_accessible :count

  ## ASSOCIATIONS ##
  belongs_to :deployment_region
  belongs_to :db_instance
end
