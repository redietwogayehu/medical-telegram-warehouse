WITH base AS (
    SELECT *
    FROM raw_staging.stg_telegram_messages
),

agg AS (
    SELECT
        channel_name,
        MIN(message_date) AS first_post_date,
        MAX(message_date) AS last_post_date,
        COUNT(*) AS total_posts,
        AVG(views) AS avg_views
    FROM base
    GROUP BY channel_name
)

SELECT
    channel_name,
    first_post_date,
    last_post_date,
    total_posts,
    avg_views
FROM agg