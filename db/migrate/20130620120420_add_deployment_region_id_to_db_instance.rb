class AddDeploymentRegionIdToDbInstance < ActiveRecord::Migration
  def change
		add_column :db_instances, :deployment_region_id, :integer
  end
end
