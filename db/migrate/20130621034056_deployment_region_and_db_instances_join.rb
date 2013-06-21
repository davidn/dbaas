class DeploymentRegionAndDbInstancesJoin < ActiveRecord::Migration
	def up
		create_table :db_instances_deployment_regions, :id => false do |t|
			t.integer :db_instance_id
			t.integer :deployment_region_id
		end
	end

	def down
		drop_table :db_instances_deployment_regions
	end
end
