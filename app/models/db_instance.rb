class DbInstance < ActiveRecord::Base
  attr_accessible :identifier, :master_username, :master_password, :allocated_storage, :provision_iops
  
  ## VALIDATIONS ##
  #validates :identifier, :presence => true
  #validates :master_username, :presence => true
  #validates :master_password, :presence => true
  
end
