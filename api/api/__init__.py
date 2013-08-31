"""Manage clusters of GenieDB nodes on cloud instances via an API.

This package does all the heavy lifting of GenieDB's DBaaS offering. It has
several modules:

* :py:mod:`~api.models` -- this defines the objects to be stored in the database.
* :py:mod:`~api.views` -- this defines the api calls the user can makes
* :py:mod:`~api.serializers` -- this defines how the models are serialized to JSON.
* :py:mod:`~api.tasks` -- this defines the asynchronous behavior
* :py:mod:`~api.admin` -- this defines the admin interface for DBaaS
* :py:mod:`~api.cloud` -- this contains an abstraction layer over EC2 and Openstack
* :py:mod:`~api.route53` -- this contains some monkeypatching over route53
* :py:mod:`~api.uuid_field` -- this defines a django field for UUIDs


This package's depencies are:

* :py:mod:`rest_framework` -- this package provides the mechanism for creating
    views in an API style. This mainly consists of viewsets (a set of views
    to provide CRUD+list operations for a given model) and serializers (a class
    defining how a model is represented as json)

* :py:mod:`celery` -- this package provides asynchronous behavior. This is used to do all
    of the setup that occurs after a node is provisioned. This includes setting
    up DNS.

* :py:mod:`boto` -- this package provides interactivity with Amazon Web Services.

* :py:mod:`novaclient` -- this package provides provisioning with OpenStack (e.g.
    Rackspace)

"""