==========
Assignment
==========

This is the most important backend for Keystone. It stores information about
roles. It also stores information about role assignment on a project/domain for
a user/group. The tables in this backend are:

* assignment
* role

assignment
==========

The table in MySql:

CREATE TABLE `assignment` (
  `type` enum('UserProject','GroupProject','UserDomain','GroupDomain') NOT NULL,
  `actor_id` varchar(64) NOT NULL,
  `target_id` varchar(64) NOT NULL,
  `role_id` varchar(64) NOT NULL,
  `inherited` tinyint(1) NOT NULL,
  PRIMARY KEY (`type`,`actor_id`,`target_id`,`role_id`),
  KEY `role_id` (`role_id`),
  KEY `ix_actor_id` (`actor_id`)
)

This table is a little difficult to map in MagetoDB because there are three
keys in MySql and MagnetoDB does not have provision of creating primary key on
more than two columns.

One solution which I have come up with is:

The table will have four columns.

* actor_id
* target_id.role_id
* target_id
* role_id
* type


| **Primary key:** (actor_id, target_id.role_id)
| **LSI:** (actor_id, target_id)
| **GSI:** (target_id), (role_id)


The idea is to make the range key such that no row will be overwritten. The
combination of two UUIDs separated by a dot are very less likely to be equal.

Operations
----------

* list_user_ids_for_project(tenant_id)

  - This can be done with GSI on project_id and then removing duplicates in
    application layer.

* create_grant(role_id, user_id=None, group_id=None, domain_id=None, project_id=None, inherited_to_projects=False)

  - This is just an insert to the table.

* list_grant_role_ids(user_id=None, group_id=None, domain_id=None, project_id=None, inherited_to_projects=False)

  - This is a query to the table on the LSI.

* check_grant_role_id(role_id, user_id=None, group_id=None, domain_id=None, project_id=None, inherited_to_projects=False)

  - This is a query on gsi role_id and then some conditional expression.
    
* delete_grant(role_id, user_id=None, group_id=None, domain_id=None, project_id=None, inherited_to_projects=False)

  - Get the grant and then delete it.

* list_project_ids_for_user(self, user_id, group_ids, hints, inherited_to_projects=False)

  - A query on key actor_id with the condition that it is of project type.

* list_domain_ids_for_user(self, user_id, group_ids, hints, inherited_to_projects=False)

  - A query on key actor_id with condition that it is of domain type.

* list_role_ids_for_groups_on_domain(self, group_ids, domain_id)

  - This is a query on the LSI.

* list_role_ids_for_groups_on_project(group_ids, project_id, project_domain_id, project_parents)

  - This would be a query on LSI. Need to find more about project_parents.

* list_project_ids_for_groups(self, group_ids, hints, inherited=False)

  - Again this would be a query on primary key or LSI.

* list_domain_ids_for_groups(self, group_ids, inherited=False)

  - This would be a query on LSI with conditionals.

* add_role_to_user_and_project(self, user_id, tenant_id, role_id)

  - An insert to the table.

* list_role_assignments()

  - A scan through the table.

* delete_project_assignments(self, project_id)

  - A query on gsi target_id followed by multiple deletes.

* delete_role_assignments(self, role_id)

  - A query on gsi role_id follwed by multiple deletes.

* delete_user(self, user_id)

  - A query on primary key followed by deletes.

* delete_group(self, group_id)

  - A query on primary key followed by deletes.

role
====
