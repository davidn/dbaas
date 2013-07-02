require 'rest_client'
require 'json'

class DbInstance < ActiveRecord::Base
  attr_accessible :identifier, :master_username, :master_password, :allocated_storage, :provision_iops,:allocated_storage
  attr_accessible :enable_automatic_backup, :backup_window, :maintenance_window, :db_instance_class
  attr_accessible :db_name, :db_port, :backup_retention_period, :daily_backup_start_time, :daily_backup_duration
  attr_accessible :region_instances_attributes, :node_size_id
  attr_accessible :provision_iops, :iops
	attr_writer :current_step
	attr_accessor :backup_window

  ## Validations ##
  validates :allocated_storage, :presence => true
  validates :identifier, :presence => true
  validates :master_username, :presence => true
  validates :master_password, :presence => true
	validates :allocated_storage, :numericality => true
	validates :node_size, :presence => true
	validates :allocated_storage, :numericality => true
	validates :iops, :numericality => {:only_integer => true, :greater_than => 0}, if: :using_iops?
  
  ## Associations ##
	belongs_to :node_size
	has_many :region_instances
  has_many :deployment_regions, :through => :region_instances

	accepts_nested_attributes_for :region_instances

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

	def using_iops?
		self.provision_iops == true
	end

	def to_json
		json = []
		self.region_instances.each do |region_instance|
			region_instance.count.times do
				this_instance = {
					:region=>region_instance.deployment_region.region_name,
					:size=>self.node_size.name,
					:storage=>self.allocated_storage
				}
				if self.using_iops?
					this_instance[:iops] = self.iops
				end
				json.push(this_instance)
			end
		end
		return json.to_json
	end

	def launch
		self.cluster_url = JSON.parse(RestClient.post(GenieDb::Application.config.DbaasApiEndpoint + 'clusters/',
			{}.to_json,
			:content_type => :json, :accept => :json,
			:Authorization => 'Token ' + GenieDb::Application.config.DbaasApiToken).body)['url']
		JSON.parse(RestClient.post(self.cluster_url,
			self.to_json,
			:content_type => :json, :accept => :json,
			:Authorization => 'Token ' + GenieDb::Application.config.DbaasApiToken).body)
		JSON.parse(RestClient.post(self.cluster_url+'launch_all/',
			{}.to_json,
			:content_type => :json, :accept => :json,
			:Authorization => 'Token ' + GenieDb::Application.config.DbaasApiToken).body)
end

	def cluster_info
		JSON.parse(RestClient.get(self.cluster_url,
			:accept => :json,
			:Authorization => 'Token ' + GenieDb::Application.config.DbaasApiToken).body)
	end

	private

	def remove_backup_params
		 if self.backup_window == "no_preference"
			 self.daily_backup_duration = nil
			 self.daily_backup_start_time = nil
		 end
	end

end
