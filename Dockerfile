FROM python:3.11-slim

COPY sys_monitor.py /app/sys_monitor.py
COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "sys_monitor.py"]
