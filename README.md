# notification-service #

Adds notification service in the library management system.

- Uses FASTAPI framework
- Consumes notification messages via Kafka
- Sends notifications to the user via email (using msmtp. Smtp exists also)
- Kafka topic: user-notifications
- Kaka broker: localhost:9092

## Usage
1. Clone the repository
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Run the app:
```
uvicorn main:app --reload --port=8002
```
Optional:
1. Change smtp details in config/email_config.py if planning to send emails via SMTP
2. Comment code on line 39-47 in `services/email_sender.py` 