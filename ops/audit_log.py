def create_audit_table(spark):
    spark.sql("""
        CREATE TABLE IF NOT EXISTS pipeline_audit_log (
            pipeline_name STRING,
            status STRING,
            record_count LONG,
            event_time TIMESTAMP
        )
        USING DELTA
    """)

def log_pipeline_status(spark, pipeline, status, record_count):
    spark.sql(f"""
        INSERT INTO pipeline_audit_log
        VALUES (
            '{pipeline}',
            '{status}',
            {record_count},
            current_timestamp()
        )
    """)