from pyspark.sql.functions import col

def run_data_quality_checks(df):
    checks = {
        "null_event_id": df.filter(col("event_id").isNull()).count(),
        "null_event_time": df.filter(col("event_time").isNull()).count()
    }

    failed = { k: v for k, v in checks.items() if v > 0 }

    if failed:
        raise Exception(f"Data quality check failed with {failed}")

    return True