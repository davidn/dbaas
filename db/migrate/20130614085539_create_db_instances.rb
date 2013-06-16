class CreateDbInstances < ActiveRecord::Migration
  def change
    create_table :db_instances do |t|
      t.string :allocated_storage
      t.boolean :provision_iops
      t.string :identifier
      t.string :master_username
      t.string :master_password
      t.boolean :enable_automatic_backup
      t.boolean :backup_window
      t.boolean :maintenance_window
      t.timestamps
    end
  end
end
