class DbInstance < ActiveRecord::Base
  attr_accessible :identifier, :master_username, :master_password, :allocated_storage, :provision_iops,:allocated_storage, :provision_iops
  attr_accessible :enable_automatic_backup, :backup_window, :maintenance_window, :db_instance_class
  attr_accessible :db_name, :db_port, :cpu_count, :ram_amount, :backup_retention_period, :daily_backup_start_time, :daily_backup_duration, :deployment_region_ids
	attr_writer :current_step
	attr_accessor :backup_window

  ## Validations ##
  validates :allocated_storage, :presence => true
  validates :identifier, :presence => true, :uniqueness => true
  validates :master_username, :presence => true
  validates :master_password, :presence => true
	validates :allocated_storage, :numericality => true
  
  ## Associations ##
  has_and_belongs_to_many :deployment_regions

	## Callbacks ##
	 before_save :remove_backup_params

	## instance methods ##
	def current_step
		@current_step || steps.first
	end

	def steps
		%w[basic management confirmation]
	end

	def next_step
		self.current_step = steps[steps.index(current_step)+1]
	end

	def previous_step
		self.current_step = steps[steps.index(current_step)-1]
	end

	def first_step?
		current_step == steps.first
	end

	def last_step?
		current_step == steps.last
	end

	private

	def remove_backup_params
		 if self.backup_window == "no_preference"
			 self.daily_backup_duration = nil
			 self.daily_backup_start_time = nil
		 end
	end
                                                                                                        
end                                                                                                     
