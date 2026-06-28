WITH base AS (
    SELECT DISTINCT DATE(message_date) AS date_day
    FROM raw_staging.stg_telegram_messages
),

final AS (
    SELECT
        date_day AS date_key,
        date_day AS full_date,
        EXTRACT(DOW FROM date_day) AS day_of_week,
        TO_CHAR(date_day, 'Day') AS day_name,
        EXTRACT(WEEK FROM date_day) AS week_of_year,
        EXTRACT(MONTH FROM date_day) AS month,
        TO_CHAR(date_day, 'Month') AS month_name,
        EXTRACT(QUARTER FROM date_day) AS quarter,
        EXTRACT(YEAR FROM date_day) AS year,
        CASE WHEN EXTRACT(DOW FROM date_day) IN (0,6) THEN TRUE ELSE FALSE END AS is_weekend
    FROM base
)

SELECT *
FROM final