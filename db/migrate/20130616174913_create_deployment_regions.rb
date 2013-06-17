class CreateDeploymentRegions < ActiveRecord::Migration
  def change
    create_table :deployment_regions do |t|
      t.string :name
      t.timestamps
    end
  end
end
