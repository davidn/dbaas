class DbInstancesDeploymentRegionsJoin < ActiveRecord::Migration
  def up

    create_table :db_instances_deployment_regions, :id => false do |t|
      t.integer :db_instance_id
      t.integer :deployment_region_id
    end

    add_index :db_instances_deployment_regions, [:db_instance_id, :deployment_region_id],
              :name => :by_db_instances_deployment_regions

  end

  def down
    drop_table :db_instances_deployment_regions
  end

end
