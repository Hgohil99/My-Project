CONFIG = {
    "stocks_to_track": ["RELIANCE.NS", "TCS.NS", "INFY.NS"],
    "metrics to monitor":[
        "current_price",
        "open_price",
        "previous_close",
        "day_high_low",
        "52_week",
        "circuit_status",
        "shareholding_pattern"
    ],
    "check_interval": "daily",
    "report_time": "18:00",
    "email_alerts": True,
    "sms_alert": True,
    "email": {
        "sender": "ypur_email@gmail.com",
        "reciever": "your_email@gmail.com",
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "password": "your_app_password"
    }
}