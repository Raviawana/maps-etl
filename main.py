from config.pipeline_metadata import PIPELINE_CONFIG
from utils.spark_session import create_spark_session
from utils.logger import get_logger

from medallion.bronze.ingest_raw import ingest_to_bronze
from medallion.silver.data_quality import run_data_quality_checks
from medallion.silver.deduplicate import deduplicate_events
from medallion.gold.business_metrics import create_gold_metrics
from ops.audit_log import create_audit_table, log_pipeline_status
from ops.recovery import get_last_successful_watermark

def main():
    spark = create_spark_session("Databricks_Spark_ETL")
    logger = get_logger("main")

    create_audit_table(spark)

    pipeline_name = "events_pipeline"
    config = PIPELINE_CONFIG[pipeline_name]

    try:
        log_pipeline_status(spark, pipeline_name, "STARTED", 0)

        last_watermark = get_last_successful_watermark(spark, pipeline_name)

        bronze_df = ingest_to_bronze(
            spark,
            config["source_path"],
            config["bronze_path"],
            last_watermark
        )

        run_data_quality_checks(bronze_df)

        silver_df = deduplicate_events(
            bronze_df,
            config["primary_key"],
            config["watermark_column"]
        )

        silver_df.write.mode("overwrite").format("delta") \
            .saveAsTable(config["silver_path"])

        create_gold_metrics(
            spark,
            config["silver_path"],
            config["gold_path"]
        )

        log_pipeline_status(
            spark,
            pipeline_name,
            "SUCCESS",
            silver_df.count()
        )

    except Exception as e:
        logger.error("Pipeline failed", exc_info=True)
        log_pipeline_status(spark, pipeline_name, "FAILED", 0)
        raise

if __name__ == "__main__":
    main()