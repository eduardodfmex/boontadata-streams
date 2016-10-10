# to do

## streaming

## short term

- update on Spark reading

## mid term 

Technologies: 
- Apache Kafka
- Apache Storm
- Apache Spark Streaming
- Apache Flink
- Apache Kafka Streams
- Apache Beam
- Apache Apex

Problems to test
- Windowing
- late arrival
- out of order events
- back pressure

The ingestion program must also generate the truth in terms of expected results. 
This data can be stored in Apache Cassandra. 
Ingestion is done in Python as this is an easy to read language, that can be modified quite simply without needing an important environment setup (like Java, Scala or C#).

IOT. Devices generate a number of measures. Each event workload will contain: 
- device id
- timestamp
- measure1
- measure2

for instance this could be cars with speed and tank level, or sensors with temperature and air pressure, etc.

Ingested events will be stored in Kafka and then can be retrieved by the consuming workloads at the speed they can. Still, ingestion must be synchronous in order to reproduce late arrival events problem.
