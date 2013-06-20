class AddBackupWindowFieldsDbInstance < ActiveRecord::Migration
  def change
    add_column :db_instances, :daily_backup_start_time, :time
    add_column :db_instances, :daily_backup_duration, :float
  end
end
