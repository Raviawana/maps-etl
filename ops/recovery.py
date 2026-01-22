def get_last_successful_watermark(spark, pipeline):
    result = spark.sql(f"""
        SELECT MAX(event_time) AS last_run
        FROM pipeline_audit_log
        WHERE pipeline_name = '{pipeline}'
          AND status = 'SUCCESS'
    """).collect()[0]["last_run"]

    return result or "1900-01-01"