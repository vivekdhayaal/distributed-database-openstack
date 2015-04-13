..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

======================
Distributed DB Backend
======================

`bp distributed-db-backend <https://blueprints.launchpad.net/keystone/+spec/distributed-database-backend>`_

The addition of an optional driver for keystone backends is proposed. This
driver is intended to be based on a NoSQL database, specifically Cassandra.

Problem Description
===================
Given that Keystone is the authN and authZ
provider for an Openstack deployment the identity, resource and assignment
information must be replicated incase there is more than one region in a 
deployment. To do that MySQL is either run in multimaster mode or master-slave
mode. If MySQL is deployed in multimaster mode than latencies for request in
any region would be much higher because all the nodes in all the regions need
to commit the data. If MySQL is run in master-slave mode then there are two
problems.
* Latency for one region is more compared to the other region where slave is
  running.
* If the master node goes down there is a risk of data loss.

Moreover MySQL, the default backend for keystone, is a single point of failure
in an Openstack deployment  which impacts availability of the Keystone service. The
replication solutions available for MySQL allow you to scale up whereas as Cassandra allows to scale out.

Proposed Change
===============

The proposal is to add a new database driver for identity, assignment and resource
backend driver which uses Cassandra. Cassandra is a truly distributed fault
tolerant database which provides high availability in spite of failures.

Alternatives
------------

None.

Security Impact
---------------

None.

Notifications Impact
--------------------

None.

Other End User Impact
---------------------

None.

Performance Impact
------------------

The performance of individual query might go down a bit at the expense of
better performance under load.

Other Deployer Impact
---------------------

This is going to be another driver. Deployers are free not to use it and
use default MySQL driver. If this driver is used then a Cassandra cluster has 
to be deployed instead of MySQL. 

* Add a new paramter cassandra_node_ips in database section.

This driver is going to reside in backend directory of each keystone backend.
So the driver should be changed for each backend if the new driver is used.

Developer Impact
----------------

None.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <ajayaa>

Other contributors:

* <rushiagr>
* <yogeshwars>
* <vivekd>

Work Items
----------

Schema design and code for following backends:

* Identity
* Credential
* Trust
* Assignment
* Token

Dependencies
============

None.

Documentation Impact
====================

The new driver needs to documented.

References
==========

* `Blueprint
  <https://blueprints.launchpad.net/keystone/+spec/distributed-database-backend>`_

* `Cassandra
  <http://cassandra.apache.org/`_
