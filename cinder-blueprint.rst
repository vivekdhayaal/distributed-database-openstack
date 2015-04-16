Distributed database backend for cinder

The rough plan is to write a NoSQL driver for cinder. The NoSQL database which we'll use is Cassandra. The main benefits of Cassandra are linear scalability, fault tolerance, high availability, reliability. We harness these benefits through the NoSQL driver.

This is an additional option and the mysql driver will continue to be the default.
