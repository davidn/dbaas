class DbInstance < ActiveRecord::Base
  attr_accessible :identifier, :master_username, :master_password, :allocated_storage, :provision_iops,:allocated_storage, :provision_iops
  attr_accessible :enable_automatic_backup, :backup_window, :maintenance_window, :db_instance_class
  attr_accessible :db_name, :db_port, :cpu_count, :ram_amount, :backup_retention_period

  ## VALIDATIONS ##
  validates :allocated_storage, :presence => true
  validates :identifier, :presence => true
  validates :master_username, :presence => true
  validates :master_password, :presence => true
                                                                                                        
end                                                                                                     
