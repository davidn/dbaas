# encoding: utf-8
# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rake db:seed (or created alongside the db with db:setup).
#
# Examples:
#
#   cities = City.create([{ name: 'Chicago' }, { name: 'Copenhagen' }])
#   Mayor.create(name: 'Emanuel', city: cities.first)


DeploymentRegion.create :name =>"US West (N. California)", :region_name=>"us-west-1"
DeploymentRegion.create :name =>"US West (Oregon)", :region_name=>"us-west-2"
DeploymentRegion.create :name =>"US East (N. Virginia)", :region_name=>"us-east-1"
DeploymentRegion.create :name =>"EU (Ireland)", :region_name=>"eu-west-1"
DeploymentRegion.create :name =>"Asia Pacific (Singapore)", :region_name=>"ap-southeast-1"
DeploymentRegion.create :name =>"Asia Pacific (Tokyo)", :region_name=>"ap-northeast-1"
DeploymentRegion.create :name =>"Asia Pacific (Sydney)", :region_name=>"ap-southeast-2"
DeploymentRegion.create :name =>"South America (São Paulo)", :region_name=>"sa-east-1"
