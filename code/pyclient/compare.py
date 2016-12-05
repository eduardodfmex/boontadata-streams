from cassandra.cluster import Cluster
from cassandra.protocol import NumpyProtocolHandler
from cassandra.query import tuple_factory
import datetime
import math
import numpy
import os
import pandas
import time
import uuid

#connect to Cassandra
cluster=Cluster(['cassandra1', 'cassandra2', 'cassandra3'])
session=cluster.connect('boontadata')
session.row_factory = tuple_factory
session.client_protocol_handler = NumpyProtocolHandler

#Compare Injector and Flink
result = session.execute(
    "SELECT window_time, device_id, category, "
    + "m1_sum_ingest_sendtime, m1_sum_ingest_devicetime, m1_sum_flink, "
    + "m2_sum_ingest_sendtime, m2_sum_ingest_devicetime, m2_sum_flink "
    + "FROM agg_events ")
df = pandas.DataFrame(result[0])
df['delta_m1_sum_ingestdevice_flink'] = df.apply(lambda row: row.m1_sum_ingest_devicetime - row.m1_sum_flink, axis=1)
df['delta_m2_sum_ingestdevice_flink'] = df.apply(lambda row: row.m2_sum_ingest_devicetime - row.m2_sum_flink, axis=1)

#disconnect from Cassandra
cluster.shutdown()

pandas.set_option('display.height', 1000)
pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 50)
pandas.set_option('display.width', 200)

print('showing all lines (not all columns) from aggregated events')
print('----------------------------------------------')
print(df
    .sort_values(by=['device_id', 'category', 'window_time'], axis=0, ascending=[True, True, True], inplace=False)
    .loc[:,['category', 'window_time', 'm1_sum_ingest_devicetime', 'm1_sum_flink', 
        'delta_m1_sum_ingestdevice_flink', 'm1_sum_ingest_sendtime', 
        'm2_sum_ingest_devicetime', 'm2_sum_flink', 
        'delta_m2_sum_ingestdevice_flink', 'm2_sum_ingest_sendtime',
        'device_id']])
print()

print('Comparing ingest device and flink for m1_sum')
print('--------------------------------------------------')
print("{} exceptions out of {}"
    .format(
        len(df.query('delta_m1_sum_ingestdevice_flink != 0').index),
        len(df.index)
    ))
print()

print('Exceptions are:')
print(
    df.query('delta_m1_sum_ingestdevice_flink != 0')
    .loc[:,['window_time', 'device_id', 'category', 'm1_sum_ingest_devicetime', 'm1_sum_flink', 'delta_m1_sum_ingestdevice_flink']]
    )

