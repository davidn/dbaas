class AddClusterUrlToDbInstance < ActiveRecord::Migration
  def change
    add_column :db_instances, :cluster_url, :string
  end
end
