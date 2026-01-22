from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, col

def deduplicate_events(df, primary_key, order_column):
    window_spec = (
        Window
        .partitionBy(primary_key)
        .orderBy(col(order_column).desc())
    )

    deduped_df = (
        df.withColumn("row_num", row_number().over(window_spec))
        .filter(col("row_num") == 1)
        .drop("row_num")
        )
    
    return deduped_df
    