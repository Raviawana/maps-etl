def create_gold_metrics(spark, silver_path, gold_table):
    spark.read.format("delta").load(silver_path) \
        .createOrReplaceTempView("silver_events")

    spark.sql(f"""
              CREATE OR REPLACE TABLE {gold_table} AS
              SELECT
              event_type,
              COUNT(*) AS total_events,
              COUNT(DISTINCT user_id) AS unique_users

              FROM silver_events

              GROUP BY event_type
              
              """)