class Initial < ActiveRecord::Migration
  def change

	  create_table :db_instances do |t|
	    t.string   :allocated_storage
	    t.boolean  :provision_iops
	    t.string   :identifier
	    t.string   :master_username
	    t.string   :master_password
	    t.boolean  :enable_automatic_backup
	    t.boolean  :backup_window
	    t.boolean  :maintenance_window
	    t.string   :db_instance_class
	    t.string   :db_name
	    t.string   :db_port
	    t.integer  :cpu_count
	    t.integer  :ram_amount
	    t.integer  :backup_retention_period
	    t.time     :daily_backup_start_time
	    t.float    :daily_backup_duration
	    t.string   :cluster_url
      t.timestamps
	  end

	  create_table :db_instances_deployment_regions, :id => false do |t|
	    t.integer :db_instance_id
	    t.integer :deployment_region_id
	  end

	  create_table :deployment_regions do |t|
	    t.string   :name
	    t.string   :region_name
      t.timestamps
	  end

  end
end
