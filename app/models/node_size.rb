class NodeSize < ActiveRecord::Base
  attr_accessible :cpu, :name, :ram
  
  has_many :db_instances
end
