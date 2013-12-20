Changelog
=========

2.5 - 2013-12-20
----------------

* Security fix. BPB-182
* Zabbix fixes. BPB-184
* Disable ALTER TABLE permissions. CFTWO-233

2.4 - 2013-12-15
------------------

* Add pricing information and credit card entry.
* Improve speed and reliability of shutdown.
* Give users choice between EBS and ephemeral disks.

2.3 - 2013-12-11
------------------

* Add unbounce webhook.
* Add email after trial ends without upgrade.

2.2.1 - 2013-12-09
------------------

* Fix SSL.

2.2 - 2013-12-04
----------------

* Shrink buffer pool size to mitigate a CloudFabric bug. CFTWO-215
* Complete grunt build system for ui. BPB-165
* Add forgot password emails. BPB-113
* Add misc API enhancements. BPB-100, BPB-93, BPB-101, BPB-88
* Add user engagement emails. BPB-154
* Some attempt to distribute AWS instances across multiple availability zones. BPB-162
* Disallow "mysql", "information_schema" and "performance_schema" databases. BPB-121
* Disable Zabbix monitoring of paused nodes. BPB-146
* Send an email when add node completes. BPB-134
