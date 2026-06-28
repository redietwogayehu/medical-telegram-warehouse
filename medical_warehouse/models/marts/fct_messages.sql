WITH m AS (
    SELECT *
    FROM raw_staging.stg_telegram_messages
),

d AS (
    SELECT *
    FROM raw_marts.dim_dates
)

SELECT
    m.message_id,
    m.channel_name,
    d.date_key,
    m.message_text,
    m.message_length,
    m.views,
    m.forwards,
    m.has_media AS has_image
FROM m
LEFT JOIN d
    ON DATE(m.message_date) = d.full_date