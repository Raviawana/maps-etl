PIPELINE_CONFIG = {
    "events_pipeline" : {
        "source_path" : "/Volumes/maps-data/bronze/raw_ingestion/event_data/",
        "bronze_path" : "`maps-data`.bronze.events",
        "silver_path" : "`maps-data`.silver.events",
        "gold_path" : "`maps-data`.gold.events",
        "load_type" : "incremental",
        "primary_key" : "event_id",
        "watermark_column" : "ingestion_time"
    }
}