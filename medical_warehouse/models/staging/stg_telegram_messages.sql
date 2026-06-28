WITH source AS (
    SELECT *
    FROM raw.telegram_messages
),

cleaned AS (
    SELECT
        message_id,
        channel_name,
        message_date::timestamp AS message_date,
        message_text,
        COALESCE(message_text, '') AS message_text_clean,
        LENGTH(COALESCE(message_text, '')) AS message_length,
        has_media,
        image_path,
        COALESCE(views, 0) AS views,
        COALESCE(forwards, 0) AS forwards
    FROM source
    WHERE message_text IS NOT NULL
)

SELECT *
FROM cleaned