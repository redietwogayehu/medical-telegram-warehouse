SELECT
    d.message_id,
    d.channel_name,
    d.image_path,
    d.detected_object,
    d.confidence,
    d.image_category,
    m.message_text,
    m.views
FROM raw.fct_image_detections d
LEFT JOIN raw.telegram_messages m
ON d.message_id = m.message_id;