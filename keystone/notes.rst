* Recently I was thinking of the situation where two simulataneous
  request from users come. For e.g. when two users simultaneously
  try to create user named aj in the same domain in keystone. If
  we don't do magnetodb operations with consistency level of cassandra
  set to quorom then two clients would see success but one of them will
  be overwritten. So it is vital to set consistency level to quorom. One
  more thing is we should check for presence of primary hash key before
  inserting a row to user table in this particular case. The reason being
  magnetodb would happily accept the request otherwise and modify the
  existing row.

* Wherever there is an unique key constraint for some columns in mysql we need to ensure
  the same in magnetodb somehow. For e.g. in user table there is unique key of
  (domain_id, name). If we don't enforce this uniqueness then we could end up having
  two users with same name in a single domain with two different ids. This gets
  complicated with the fact that in GSI uniqueness on a row is not enforced. The key
  from GSI table is the columns in GSI plus the columns of the primary key. There are
  three ways to solve it.

  * Use gsi of MagnetoDB. This is going to be eventually consistent. Before inserting
    We need to check for presence of values in gsi column. If it's there don't insert
    it and return failure to the client. If it's not there then insert it and wait
    for it to appear in gsi before returning to the client. A distributed lock is
    needed here as there could be race conditions. Distributed because there could
    be multiple nodes having the same role and trying the same kind of operations.
    For e.g. there could be multiple keystone nodes.

  * Use a separate table created manullay for gsi. Here we need to insert in the
    gsi table first and then in the main table. Similar to the above point we need
    to check the gsi table first and then if not present then insert the data. Here
    also we would need a distributed lock.

  * Investigate why the component needs an unique field on a column different than
    the primary key. At least in the case of keystone it is pretty evident that
    the user in User table has to be unique because while getting a token the user
    specifies user, password and project. So the flow goes something like this:
    First keystone gets the user_id based on user_name and then gets the project_id
    based on the project_name and domain_name. Then it goes to assignment backend
    and gets the role and then to token backend to get a token. At least in this
    case we can't do away with uniqueness constraint unless we make the token
    creation process based on the id's instead of user_name and project_name.

  * When using a (domain_id, name) combination as primary key for user table, all
    the users having same domain_id would end up in one partition. So if we are
    not using domain feature at all, then it sounds like a bad design.


