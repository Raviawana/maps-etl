from pyspark.sql.types import (
    StructType, StructField, StringType, TimestampType
)


EVENT_SCHEMA = StructType([
    StructField("event_id", StringType(), False),
    StructField("user_id", StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("event_time", TimestampType(), True),
    StructField("ingestion_time", TimestampType(), True)
    ])