..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

======================
Distributed DB Backend
======================

`bp distributed-db-backend <https://blueprints.launchpad.net/cinder/+spec/distributed-database-backend>`_

The addition of an optional driver for cinder database backend is proposed.
This driver is intended to be based on a NoSQL database, i.e, Cassandra.

Problem Description
===================

The aspects where NoSQL databases outperform relational databases
are explained in detail in the wiki @
https://wiki.openstack.org/wiki/NoSQL

In short, a NoSQL database outscores a SQL database in the below aspects,
* Horizonal scalability/centralized architecture
* Availability
* Reliability

Use Cases
=========

None

Proposed Change
===============

The proposal is to add a new database driver for cinder which uses Cassandra.
Cassandra is a distributed database that offers linear scalability, fault-
tolerance, high availability and reliability.

Alternatives
------------

None.

Data model impact
-----------------

None

REST API impact
---------------

None

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

Better performance under load.
The performance of a query under no-load might have to be traded off.

Other Deployer Impact
---------------------

This is just another driver residing in the cinder backend directory.
Deployers are free not to use it and use default MySQL driver.
If this driver is used then a Cassandra cluster and associated client
libraries have to be deployed. 

* Add a new paramter cassandra_node_ips in database section.
* Add the cassandra driver path to use it instead of the default MySQL driver.

Developer Impact
----------------

None.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <vivekdhayaal>

Other contributors:

* <rushiagr>
* <ajayaa>
* <yogeshwars>

Work Items
----------

Schema design and code for the new database driver

Dependencies
============

None.

Testing
=======

None.

Documentation Impact
====================

The new driver needs to documented.

References
==========

* `Blueprint
  <https://blueprints.launchpad.net/cinder/+spec/distributed-database-backend>`_

* `Cassandra
  <http://cassandra.apache.org/`_
