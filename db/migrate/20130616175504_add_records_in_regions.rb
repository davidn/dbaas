class AddRecordsInRegions < ActiveRecord::Migration
  def up
    DeploymentRegion.create :name =>"Virginia"
    DeploymentRegion.create :name =>"California"
    DeploymentRegion.create :name =>"Singapore"
    DeploymentRegion.create :name =>"India"
  end

  def down
    DeploymentRegion.delete_all
  end
end
