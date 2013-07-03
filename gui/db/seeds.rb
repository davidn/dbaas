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

NodeSize.create :name => "t1.micro",		:cpu => 1,	:ram => 1
NodeSize.create :name => "m1.small",		:cpu => 1,	:ram => 2
NodeSize.create :name => "m1.medium",		:cpu => 1,	:ram => 4
NodeSize.create :name => "m1.large",		:cpu => 2,	:ram => 8
NodeSize.create :name => "m1.xlarge",		:cpu => 4,	:ram => 16
NodeSize.create :name => "m3.xlarge",		:cpu => 4,	:ram => 16
NodeSize.create :name => "m3.2xlarge",	:cpu => 8,	:ram => 32
NodeSize.create :name => "c1.medium",		:cpu => 2,	:ram => 2
NodeSize.create :name => "c1.xlarge",		:cpu => 8,	:ram => 8
NodeSize.create :name => "cc2.8xlarge",	:cpu => 32,	:ram => 64
NodeSize.create :name => "m2.xlarge",		:cpu => 2,	:ram => 16
NodeSize.create :name => "m2.2xlarge",	:cpu => 4,	:ram => 32
NodeSize.create :name => "m2.4xlarge",	:cpu => 8,	:ram => 64
NodeSize.create :name => "cr1.8xlarge",	:cpu => 32,	:ram => 224
NodeSize.create :name => "hi1.4xlarge",	:cpu => 16,	:ram => 64
NodeSize.create :name => "hs1.8xlarge",	:cpu => 16,	:ram => 117
NodeSize.create :name => "cg1.4xlarge",	:cpu => 32,	:ram => 16
