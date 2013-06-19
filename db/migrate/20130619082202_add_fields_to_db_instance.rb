class AddFieldsToDbInstance < ActiveRecord::Migration
  def change
    add_column :db_instances, :db_instance_class, :string
    add_column :db_instances, :db_name, :string
    add_column :db_instances, :db_port, :string
    add_column :db_instances, :cpu_count, :integer
    add_column :db_instances, :ram_amount, :integer
    add_column :db_instances, :backup_retention_period, :integer
  end
end
