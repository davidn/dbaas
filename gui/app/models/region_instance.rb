class RegionInstance < ActiveRecord::Base
  attr_accessible :count, :db_instance, :deployment_region, :deployment_region_id

  ## ASSOCIATIONS ##
  belongs_to :deployment_region
  belongs_to :db_instance
end
