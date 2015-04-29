========
Cinder
========

Cinder implements services and libraries to provide on demand,
self-service access to Block Storage resources.

+--------------------------+
| Tables_in_cinder         |
+--------------------------+
| backups                  |
| cgsnapshots              |
| consistencygroups        |
| driver_initiator_data    |
| encryption               |
| iscsi_targets            |
| migrate_version          |
| quality_of_service_specs |
| quota_classes            |
| quota_usages             |
| quotas                   |
| reservations             |
| services                 |
| snapshot_metadata        |
| snapshots                |
| transfers                |
| volume_admin_metadata    |
| volume_attachment        |
| volume_glance_metadata   |
| volume_metadata          |
| volume_type_extra_specs  |
| volume_type_projects     |
| volume_types             |
| volumes                  |
+--------------------------+


volumes
=======

The five tables pertaining to volumes have the below schema in MySql.

CREATE TABLE `volumes` (
  `created_at` datetime DEFAULT NULL>,
  `updated_at` datetime DEFAULT NULL>,
  `deleted_at` datetime DEFAULT NULL>,
  `deleted` tinyint(1) DEFAULT NULL>,
  `id` varchar(36) NOT NULL>,
  `ec2_id` varchar(255) DEFAULT NULL>,
  `user_id` varchar(255) DEFAULT NULL>,
  `project_id` varchar(255) DEFAULT NULL>,
  `host` varchar(255) DEFAULT NULL>,
  `size` int(11) DEFAULT NULL>,
  `availability_zone` varchar(255) DEFAULT NULL>,
  `status` varchar(255) DEFAULT NULL>,
  `attach_status` varchar(255) DEFAULT NULL>,
  `scheduled_at` datetime DEFAULT NULL>,
  `launched_at` datetime DEFAULT NULL>,
  `terminated_at` datetime DEFAULT NULL>,
  `display_name` varchar(255) DEFAULT NULL>,
  `display_description` varchar(255) DEFAULT NULL>,
  `provider_location` varchar(256) DEFAULT NULL>,
  `provider_auth` varchar(256) DEFAULT NULL>,
  `snapshot_id` varchar(36) DEFAULT NULL>,
  `volume_type_id` varchar(36) DEFAULT NULL>,
  `source_volid` varchar(36) DEFAULT NULL>,
  `bootable` tinyint(1) DEFAULT NULL>,
  `provider_geometry` varchar(255) DEFAULT NULL>,
  `_name_id` varchar(36) DEFAULT NULL>,
  `encryption_key_id` varchar(36) DEFAULT NULL>,
  `migration_status` varchar(255) DEFAULT NULL>,
  `replication_status` varchar(255) DEFAULT NULL>,
  `replication_extended_status` varchar(255) DEFAULT NULL>,
  `replication_driver_data` varchar(255) DEFAULT NULL>,
  `consistencygroup_id` varchar(36) DEFAULT NULL>,
  `provider_id` varchar(255) DEFAULT NULL>,
  `multiattach` tinyint(1) DEFAULT NULL>,
  PRIMARY KEY (`id`)>,
  KEY `consistencygroup_id` (`consistencygroup_id`)>,
  CONSTRAINT `volumes_ibfk_1` FOREIGN KEY (`consistencygroup_id`) REFERENCES `consistencygroups` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `volume_attachment` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` varchar(36) NOT NULL,
  `volume_id` varchar(36) NOT NULL,
  `attached_host` varchar(255) DEFAULT NULL,
  `instance_uuid` varchar(36) DEFAULT NULL,
  `mountpoint` varchar(255) DEFAULT NULL,
  `attach_time` datetime DEFAULT NULL,
  `detach_time` datetime DEFAULT NULL,
  `attach_mode` varchar(36) DEFAULT NULL,
  `attach_status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `volume_id` (`volume_id`),
  CONSTRAINT `volume_attachment_ibfk_1` FOREIGN KEY (`volume_id`) REFERENCES `volumes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `volume_metadata` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `volume_id` varchar(36) NOT NULL,
  `key` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `volume_id` (`volume_id`),
  CONSTRAINT `volume_metadata_ibfk_1` FOREIGN KEY (`volume_id`) REFERENCES `volumes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `volume_glance_metadata` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `volume_id` varchar(36) DEFAULT NULL,
  `snapshot_id` varchar(36) DEFAULT NULL,
  `key` varchar(255) DEFAULT NULL,
  `value` text,
  PRIMARY KEY (`id`),
  KEY `volume_id` (`volume_id`),
  KEY `snapshot_id` (`snapshot_id`),
  CONSTRAINT `volume_glance_metadata_ibfk_1` FOREIGN KEY (`volume_id`) REFERENCES `volumes` (`id`),
  CONSTRAINT `volume_glance_metadata_ibfk_2` FOREIGN KEY (`snapshot_id`) REFERENCES `snapshots` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `volume_admin_metadata` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `volume_id` varchar(36) NOT NULL,
  `key` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `volume_id` (`volume_id`),
  CONSTRAINT `volume_admin_metadata_ibfk_1` FOREIGN KEY (`volume_id`) REFERENCES `volumes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

The volumes table looks the almost same in MagnetoDB with the addition of four more columns

* volume_type_name - to prevent join with volume_type table while fetching volume list
* volume_metadata - key:value properties map - to prevent join with volume_metadata table 
* volume_admin_metadata - key:value admin properties map - to prevent join with volume_Admin_metadata table
* volume_attachment - attachments list - to prevent join with volume_attachment table; this would mean that volume attachment operations need to update in two tables, volumes & volume_attachment

The volume_attachment table look the same in MagnetoDB as well.

The volume_metadata, volume_admin_metadata and volume_glance_metadata tables contain two columns each; the first being the property and the second being the list of volumes associated with that. volume_glance_metadata table additionally has a list of snapshots as well. This is to support querying volumes/snapshots associated with a given property. This would mean that metadata related operations need to update in two tables, volumes & any one of volume*metadata

Operations: REST API - DB API
-----------------------------

cinder create - get_volume_type_by_name, get_volume_type, quoto_reserve,volume_create,reservation_commit

cinder delete - snapshot_get_all_for_volume; can't delete if snapshots exist; volume_glance_metadata_delete_by_volume, volume_destroy

cinder extend - quota_reserve,volume_update,reservation_commit

cinder force-delete

cinder list - volume_get_all or volume_get_all_by_project

cinder metadata - volume_metadata_update

cinder metadata-show - volume_metadata_get

cinder metadata-update-all - volume_metadata_update

cinder migrate - volume_update

nova volume-attach - get_volume,volume_attach,volume_attachment_get_by_instance_uuid(filter=vol_id,inst_uuid,attch_status) or volume_attachment_get_by_host, volume_attach,volume_attachment_update,volume_attached,volume_update,volume_attachment_get

nova volume-create

nova volume-delete

nova volume-detach - volume_attachment_get or volume_attachment_get_used_by_volume_id,volume_get,volume_detached,volume_admin_metadata_delete(attached_mode),volume_get

nova volume-list

nova volume-show - volume_get

nova volume-update


* volume_attach(context, values) - create new volume attachment

* volume_attached(context, attachment_id, instance_uuid, host_name, mountpoint, attach_mode='rw') - update volume attachment entry

* volume_create(context, values)

* volume_data_get_for_host(context, host, count_only=False) - create secondary index on host column or create new table that acts as an index

* volume_data_get_for_project(context, project_id, volume_type_id=None) - create secondary index on project_id column or create new table  that acts as an index

* finish_volume_migration(context, src_vol_id, dest_vol_id) - update a volume row's migration related colums

* volume_destroy(context, volume_id)

* volume_detach(context, attachment_id)

* volume_detached(context, volume_id, attachment_id)

* volume_attachment_get(context, attachment_id, session=None)

* volume_attachment_get_used_by_volume_id(context, volume_id, session=None)

* volume_attachment_get_by_host(context, volume_id, host) - create secondary index on host column or create new table  that acts as an index

* volume_attachment_get_by_instance_uuid(context, volume_id, instance_uuid) - create secondary index on uuid column or create new table that acts as an index

* volume_get(context, volume_id)

* volume_get_all(context, marker, limit, sort_keys=None, sort_dirs=None, filters=None) - In SQL, using joins, query volume based on any column in volumes table or key:value in volume_metadata/volume_admin_metadata tables. In MagnetoDB, in case of multiple filters, we can fetch all volumes associated with given metadata from volume*metadata table and the scan the volumes table to apply the remaining filters.

* volume_get_all_by_host(context, host, filters=None) - create secondary index on host column or create new table  that acts as an index

* volume_get_all_by_group(context, group_id, filters=None) - create secondary index on group column or create new table  that acts as an index

* volume_get_all_by_project(context, project_id, marker, limit, sort_keys=None, sort_dirs=None, filters=None) - create secondary index on project column or create new table  that acts as an index

* volume_update(context, volume_id, value)

* volume_attachment_update(context, attachment_id, values)

* volume_metadata_get_item(context, volume_id, key)

* volume_metadata_get(context, volume_id)

* volume_metadata_delete(context, volume_id, key)

* volume_metadata_update(context, volume_id, metadata, delete)

* volume_admin_metadata_get(context, volume_id)

* volume_admin_metadata_delete(context, volume_id, key)

* volume_admin_metadata_update(context, volume_id, metadata, delete)

* volume_glance_metadata_get_all(context)

* volume_glance_metadata_get(context, volume_id)

* volume_snapshot_glance_metadata_get(context, snapshot_id)

* volume_glance_metadata_create(context, volume_id, key, value)

* volume_glance_metadata_copy_to_snapshot(context, snapshot_id, volume_id)

* volume_glance_metadata_copy_from_volume_to_volume(context, src_volume_id, volume_id)

* volume_glance_metadata_copy_to_volume(context, volume_id, snapshot_id)

* volume_glance_metadata_delete_by_volume(context, volume_id)

* volume_glance_metadata_delete_by_snapshot(context, snapshot_id)


volume_types
============

The four tables pertaining to volume_type have the below schema in MySQL.

CREATE TABLE `volume_types` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` varchar(36) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `qos_specs_id` varchar(36) DEFAULT NULL,
  `is_public` tinyint(1) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `qos_specs_id` (`qos_specs_id`),
  CONSTRAINT `volume_types_ibfk_1` FOREIGN KEY (`qos_specs_id`) REFERENCES `quality_of_service_specs` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `volume_type_projects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `volume_type_id` varchar(36) DEFAULT NULL,
  `project_id` varchar(255) DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `volume_type_id` (`volume_type_id`,`project_id`,`deleted`),
  CONSTRAINT `volume_type_projects_ibfk_1` FOREIGN KEY (`volume_type_id`) REFERENCES `volume_types` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `volume_type_extra_specs` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `volume_type_id` varchar(36) NOT NULL,
  `key` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `volume_type_extra_specs_ibfk_1` (`volume_type_id`),
  CONSTRAINT `volume_type_extra_specs_ibfk_1` FOREIGN KEY (`volume_type_id`) REFERENCES `volume_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8

CREATE TABLE `quality_of_service_specs` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` varchar(36) NOT NULL,
  `specs_id` varchar(36) DEFAULT NULL,
  `key` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `specs_id` (`specs_id`),
  CONSTRAINT `quality_of_service_specs_ibfk_1` FOREIGN KEY (`specs_id`) REFERENCES `quality_of_service_specs` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8


The volume_type_extra_specs & volume_type_projects tables are merged with volumes table with the addition of new columns.

* volume_type_extra_specs - key:value map - to associate volume_types with extra_specs 

* volume_type_projects - list of projects in which this volume type is exposed

The quality_of_service_specs table in MagnetoDB shall have three columns uuid, name and map of specs. To support the query to fetch all volume_types associated with a given qos_spec, we can either create a secondary index on qos_specs_id column in volume_types table or add a new column 'volume_types' in quality_of_service_specs tables that contains a list of associated volume_types.

Operations: REST API - DB API
-----------------------------

cinder type-create - volume_type_create

cinder type-delete - volume_type_update

cinder type-key - volume_type_extra_specs_update_or_create

cinder type-list - volume_type_get_all

cinder qos-associate - volume_type_qos_associate

cinder qos-create - qos_specs_create,get_qos_specs_by_name,qos_specs_update

cinder qos-delete - qos_specs_delete

cinder qos-disassociate - volume_type_qos_disassociate

cinder qos-disassociate-all - volume_type_qos_disassociate_all

cinder qos-get-association - qos_specs_associations_get

cinder qos-key - qos_specs_update,qos_specs_item_delete

cinder qos-list - qos_specs_get_all

cinder qos-show - qos_specs_get

nova volume-type-create

nova volume-type-delete

nova volume-type-list


* volume_type_create(context, values, projects=None)

* volume_type_update(context, volume_type_id, values)

* volume_type_get_all(context, inactive=False, filters=None) - supported filter 'is_public'; 

* volume_type_get(context, id, inactive=False, expected_fields=None)

* volume_type_get_by_name(context, name)

* volume_types_get_by_name_or_id(context, volume_type_list)

* volume_type_qos_associations_get(context, qos_specs_id, inactive=False) - get all volumes associated with a qos spec

* volume_type_qos_associate(context, type_id, qos_specs_id)

* volume_type_qos_disassociate(context, qos_specs_id, type_id)

* volume_type_qos_disassociate_all(context, qos_specs_id)

* volume_type_qos_specs_get(context, type_id) - get the qos spec associated with a volume_type

* volume_type_destroy(context, id)

* volume_type_access_get_all(context, type_id) - get all projects in which the given volume_type is exposed

* volume_type_access_add(context, type_id, project_id)

* volume_type_access_remove(context, type_id, project_id)

* volume_type_extra_specs_get(context, volume_type_id)

* volume_type_extra_specs_delete(context, volume_type_id, key)

* volume_type_extra_specs_update_or_create(context, volume_type_id, specs)

* qos_specs_create(context, values)

* qos_specs_get(context, qos_specs_id, inactive=False)

* qos_specs_get_all(context, inactive=False, filters=None)

* qos_specs_get_by_name(context, name, inactive=False) - create secondary index on name column or create new table  that acts as an index

* qos_specs_associations_get(context, qos_specs_id) - get all volume_types associated with the given qos_specs_id

* qos_specs_associate(context, qos_specs_id, type_id)

* qos_specs_disassociate(context, qos_specs_id, type_id)

* qos_specs_disassociate_all(context, qos_specs_id)

* qos_specs_item_delete(context, qos_specs_id, key)

* qos_specs_delete(context, qos_specs_id)

* qos_specs_update(context, qos_specs_id, specs)
 

snapshots
=========

The two tables associated with snapshots have the below schema in MySQL.

CREATE TABLE `snapshots` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` varchar(36) NOT NULL,
  `volume_id` varchar(36) NOT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `project_id` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `progress` varchar(255) DEFAULT NULL,
  `volume_size` int(11) DEFAULT NULL,
  `scheduled_at` datetime DEFAULT NULL,
  `display_name` varchar(255) DEFAULT NULL,
  `display_description` varchar(255) DEFAULT NULL,
  `provider_location` varchar(255) DEFAULT NULL,
  `encryption_key_id` varchar(36) DEFAULT NULL,
  `volume_type_id` varchar(36) DEFAULT NULL,
  `cgsnapshot_id` varchar(36) DEFAULT NULL,
  `provider_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `snapshots_volume_id_fkey` (`volume_id`),
  KEY `cgsnapshot_id` (`cgsnapshot_id`),
  CONSTRAINT `snapshots_ibfk_1` FOREIGN KEY (`cgsnapshot_id`) REFERENCES `cgsnapshots` (`id`),
  CONSTRAINT `snapshots_volume_id_fkey` FOREIGN KEY (`volume_id`) REFERENCES `volumes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `snapshot_metadata` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `snapshot_id` varchar(36) NOT NULL,
  `key` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `snapshot_id` (`snapshot_id`),
  CONSTRAINT `snapshot_metadata_ibfk_1` FOREIGN KEY (`snapshot_id`) REFERENCES `snapshots` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

The snapshot_metadata table is merged with snapshots table with the addition of new column.

* snapshot_metadata - key:value properties map

Operations: REST API - DB API
-----------------------------

cinder snapshot-create - snapshot_create

cinder snapshot-delete - snapshot_destroy

cinder snapshot-list - allowed_search_options = ('status', 'volume_id', 'name') - snapshot_get_all or snapshot_get_all_by_project

cinder snapshot-metadata - snapshot_metadata_update

cinder snapshot-metadata-show  - snapshot_metadata_get

cinder snapshot-metadata-update-all - snapshot_metadata_update

cinder snapshot-rename - snapshot_update

cinder snapshot-reset-state - snapshot_update

cinder snapshot-show - snapshot_get


* snapshot_create(context, values)

* snapshot_destroy(context, snapshot_id)

* snapshot_get(context, snapshot_id)

* snapshot_get_all(context)

* snapshot_get_all_for_volume(context, volume_id) - create secondary index on volume column or create new table  that acts as an index

* snapshot_get_all_for_cgsnapshot(context, cgsnapshot_id) - create secondary index on cgsnapshot column or create new table  that acts as an index

* snapshot_get_all_by_project(context, project_id) - create secondary index on project column or create new table  that acts as an index

* snapshot_data_get_for_project(context, project_id, volume_type_id=None)

* snapshot_update(context, snapshot_id, values)

* snapshot_metadata_get(context, snapshot_id)

* snapshot_metadata_delete(context, snapshot_id, key)

* snapshot_metadata_update(context, snapshot_id, metadata, delete)



consistencygroups
=================

The two tables associated with snapshots have the below schema in MySQL.

CREATE TABLE `consistencygroups` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` varchar(36) NOT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `project_id` varchar(255) DEFAULT NULL,
  `host` varchar(255) DEFAULT NULL,
  `availability_zone` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `volume_type_id` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `cgsnapshot_id` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `cgsnapshots` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` varchar(36) NOT NULL,
  `consistencygroup_id` varchar(36) NOT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `project_id` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `consistencygroup_id` (`consistencygroup_id`),
  CONSTRAINT `cgsnapshots_ibfk_1` FOREIGN KEY (`consistencygroup_id`) REFERENCES `consistencygroups` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

These two tables look the same in MagnetoDB as well. 

consistency group create (using volume types) - get_volume_type_qos_specs
consistency group create from src - cgsnapshot_get,consistencygroup_get,consistencygroup_create, snapshot_get_all_for_cgsnapshot,volume_create,consistencygroup_destroy,volume_get_all_by_group,volume_update,
consistency group delete - snapshot_get_all_for_volume


Operations
----------

* consistencygroup_data_get_for_project(context, project_id) - create secondary index on project column or create new table  that acts as an index

* consistencygroup_get(context, consistencygroup_id)

* consistencygroup_get_all(context)

* consistencygroup_get_all_by_project(context, project_id)

* consistencygroup_create(context, values)

* consistencygroup_update(context, consistencygroup_id, values)

* consistencygroup_destroy(context, consistencygroup_id)

* cgsnapshot_get(context, cgsnapshot_id)

* cgsnapshot_get_all(context)

* cgsnapshot_get_all_by_group(context, group_id) - create secondary index on group column or create new table  that acts as an index

* cgsnapshot_get_all_by_project(context, project_id) - create secondary index on project column or create new table  that acts as an index

* cgsnapshot_create(context, values)

* cgsnapshot_update(context, cgsnapshot_id, values)

* cgsnapshot_destroy(context, cgsnapshot_id)


quotas
======

The four tables associated with quotas have the below schema in MySQL:

CREATE TABLE `quotas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `project_id` varchar(255) DEFAULT NULL,
  `resource` varchar(255) NOT NULL,
  `hard_limit` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `quota_classes` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `class_name` varchar(255) DEFAULT NULL,
  `resource` varchar(255) DEFAULT NULL,
  `hard_limit` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_quota_classes_class_name` (`class_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8

CREATE TABLE `quota_usages` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` varchar(255) DEFAULT NULL,
  `resource` varchar(255) DEFAULT NULL,
  `in_use` int(11) NOT NULL,
  `reserved` int(11) NOT NULL,
  `until_refresh` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_quota_usages_project_id` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8

CREATE TABLE `reservations` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(36) NOT NULL,
  `usage_id` int(11) NOT NULL,
  `project_id` varchar(255) DEFAULT NULL,
  `resource` varchar(255) DEFAULT NULL,
  `delta` int(11) NOT NULL,
  `expire` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usage_id` (`usage_id`),
  KEY `ix_reservations_project_id` (`project_id`),
  KEY `reservations_deleted_expire_idx` (`deleted`,`expire`),
  CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`usage_id`) REFERENCES `quota_usages` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8

These four tables have the same schema in MagnetoDB as well.

Operations: REST API - DB API
-----------------------------

cinder quota-class-show - quota_class_get_all_by_name(context, quota_class),quota_class_get_default(context)

cinder quota-class-update - quota_class_update

cinder quota-defaults - quota_class_get_default, 

cinder quota-delete - quota_destroy_all_by_project

cinder quota-show - quota_get_all_by_project(context, project_id)

cinder quota-update - quota_update

cinder quota-usage - quota_usage_get_all_by_project


* quota_get(context, project_id, resource)

* quota_get_all_by_project(context, project_id) - create secondary index on project column or create new table  that acts as an index

* quota_create(context, project_id, resource, limit)

* quota_update(context, project_id, resource, limit)

* quota_destroy(context, project_id, resource)

* quota_class_get(context, class_name, resource)

* quota_class_get_default(context) - query.filter_by(class_name=_DEFAULT_QUOTA_NAME) - create secondary index on quota_class column or create new table  that acts as an index

* quota_class_get_all_by_name(context, class_name)

* quota_class_create(context, class_name, resource, limit)

* quota_class_update(context, class_name, resource, limit)

* quota_class_destroy(context, class_name, resource)

* quota_class_destroy_all_by_name(context, class_name)

* quota_usage_get(context, project_id, resource)

* quota_usage_get_all_by_project(context, project_id) - create secondary index on project column or create new table  that acts as an index

* quota_reserve(context, resources, quotas, deltas, expire, until_refresh, max_age, project_id=None)

* quota_destroy_all_by_project(context, project_id)

* reservation_commit(context, reservations, project_id=None) - update a reservation entry

* reservation_rollback(context, reservations, project_id=None) - update a reservation entry

* reservation_expire(context) - update a reservation entry


Rest
====
The remaining seven tables have the same schema in MagnetoDB as well:
backups, driver_initiator_data, encryption, iscsi_targets, migrate_version, services, transfers
