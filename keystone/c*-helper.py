from cassandra.cluster import Cluster
import re

cluster = Cluster(['127.0.0.1', '127.0.0.2', '127.0.0.3'])
session = cluster.connect()
#r = session.execute("create keyspace aj with replication = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };")

def flush(tables):
    r = session.execute("select name, internal_name from magnetodb.\
            table_info where tenant='default_tenant'")
    r1 = [ row.internal_name for row in r if row.name in tables]
    internal_names = []
    for ele in r1:
        internal_names.append(re.sub('["]', '', ele))
    for table in internal_names:
        r = session.execute("truncate " + table + ";")

def select(tables):
    r = session.execute("select name, internal_name from magnetodb.\
            table_info where tenant='default_tenant'")
    r1 = [ row.internal_name for row in r if row.name in tables]
    internal_names = []
    for ele in r1:
        internal_names.append(re.sub('["]', '', ele))
    for table in internal_names:
        r = session.execute("select * from "+ table + ";")
        print r
        print

def get_names(tables):
    r = session.execute("select name, internal_name from magnetodb.\
            table_info where tenant='default_tenant'")
    r1 = [ row.internal_name for row in r if row.name in tables]
    internal_names = []
    for ele in r1:
        internal_names.append(re.sub('["]', '', ele))
    print internal_names
    return internal_names
