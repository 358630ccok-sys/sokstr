import os
import requests

def get_system_info():
    import psutil
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk_free = psutil.disk_usage('/').free / (1024 ** 3)
    return {
        "cpu": cpu_usage,
        "ram": memory.percent,
        "disk": disk_free
    }

def send_to_telegram(message, chat_id):
    token = os.getenv("TELEGRAM_TOKEN")
    response_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        requests.post(response_url, json=payload)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def main():
    system_info = get_system_info()
    message = (f"CPU Usage: {system_info['cpu']}%\n"
               f"RAM Usage: {system_info['ram']}%\n"
               f"Disk Free: {round(system_info['disk'], 2)} GB")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    send_to_telegram(message, chat_id)

if __name__ == "__main__":
    main()
