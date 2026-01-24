from pyspark.sql.functions import col
from schemas.source_schema import EVENT_SCHEMA


def ingest_to_bronze(spark, source_path, bronze_path, last_watermark):
    df = (
        spark.read
        .schema(EVENT_SCHEMA)
        .parquet(source_path)
        .filter(col("ingestion_time") > last_watermark)
    )

    (
    df.write
    .mode("append")
    .format("delta")
    .saveAsTable(bronze_path)
    )
    
    return df