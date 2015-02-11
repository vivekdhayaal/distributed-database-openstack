========
Identity
========

The first backend which we started moving is Identity. It stores information 
about users and groups in Keystone. Groups are a way to aggregate users into 
different groups. Assigning a role to a group is equivalent to assigning all
the users of that group that role. The tables with which this backend interacts
are:

* user
* group
* user_group_membership

user
====

The table for user looks something like this in MySql.

CREATE TABLE `user` (
  `id` varchar(64) NOT NULL,
  `name` varchar(255) NOT NULL,
  `extra` text,
  `password` varchar(128) DEFAULT NULL,
  `enabled` tinyint(1) DEFAULT NULL,
  `domain_id` varchar(64) NOT NULL,
  `default_project_id` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ixu_user_name_domain_id` (`domain_id`,`name`),
  CONSTRAINT `fk_user_domain_id` FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`)
)

This table looks the same in MagnetoDB with the exception that the primary key 
is (`domain_id`, `name`) and there is a GSI on id field. This was done to keep 
domain_id and name pair unique.

Operations
----------

* create_user(user_id, user)

* delete_user(user_id)

* update_user(domain_id, user_id, user)

* get_user(user_id)

* get_user_by_name(domain_id, name)

* list_users(domain_id)

All the operations mentioned here don't need explanation really.

group
=====

The table for group looks similar to the above user table except there is no
`password` and `default_project_id` field in the table.

Operations
----------

The operations here also look similar to operations in user table. Just replace
`user_id` with `group_id` and `user` with `group`.

user_group_membership
=====================

This table looks like the following in MySql.

CREATE TABLE `user_group_membership` (
  `user_id` varchar(64) NOT NULL,
  `group_id` varchar(64) NOT NULL,
  PRIMARY KEY (`user_id`,`group_id`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `fk_user_group_membership_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `fk_user_group_membership_group_id` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`)
)

This table can look the same in MagnetoDB but there are concerns over the same
columns appearing twice in the GSI table.

Operations
----------

* add_user_to_group(user_id, group_id)

* check_user_in_group(user_id, group_id)

* remove_user_from_group(user_id, group_id)

* list_users_in_group(group_id)

* list_groups_for_user(group_id)
