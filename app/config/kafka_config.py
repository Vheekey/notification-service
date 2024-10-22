class KafkaConfig:
    BOOTSTRAP_SERVERS = "127.0.0.1:9092"
    GROUP_ID = "notification_service"
    TOPIC = "user-notifications"
    AUTO_OFFSET_RESET = "earliest"
