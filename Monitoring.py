import psutil
import time
import json
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess

# Configurations
CPU_THRESHOLD = 85  # % CPU usage threshold
MEMORY_THRESHOLD = 85  # % Memory usage threshold
LATENCY_THRESHOLD = 200  # ms Latency threshold
APP_OVERHEAD_THRESHOLD = 100  # ms Application overhead threshold
EMAIL_RECIPIENT = "alerts@company.com"
EMAIL_SENDER = "monitoring@company.com"
SMTP_SERVER = "smtp.company.com"
SMTP_PORT = 587
SMTP_PASSWORD = "your_email_password"

# Function to send alert email
def send_alert_email(subject, message):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECIPIENT
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, text)
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to get system metrics
def get_system_metrics():
    # CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)

    # Memory usage
    memory = psutil.virtual_memory()
    memory_usage = memory.percent

    # Network latency using ping to google.com
    try:
        ping_response = subprocess.run(
            ["ping", "-c", "1", "google.com"],
            capture_output=True,
            text=True
        )
        latency = int(ping_response.stdout.split("time=")[-1].split(" ms")[0])
    except Exception as e:
        print(f"Error checking latency: {e}")
        latency = 999  # Default high latency if ping fails

    # Database contention (simulated check for active database connections)
    db_contention = 1 if check_database_contention() else 0

    # Application Layer Overhead (simulated with a sample API request)
    try:
        app_response = requests.get("https://api.github.com", timeout=5)
        app_overhead = int(app_response.elapsed.total_seconds() * 1000)  # ms
    except requests.RequestException as e:
        print(f"Error checking application overhead: {e}")
        app_overhead = 999  # Default high overhead if request fails

    # Log the metrics
    metrics = {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "latency": latency,
        "db_contention": db_contention,
        "app_overhead": app_overhead
    }

    return metrics

# Simulated function to check for database contention
def check_database_contention():
    # Here you would add actual database query logic to detect contention
    # For example, you might query the number of active connections or locks
    # Return True if contention detected, otherwise False
    return False  # Placeholder

# Function to monitor system
def monitor_system():
    while True:
        metrics = get_system_metrics()

        # Log the metrics in JSON format
        with open("system_metrics_log.json", "a") as f:
            json.dump(metrics, f)
            f.write("\n")

        # Check if thresholds are exceeded and trigger alert
        if metrics["cpu_usage"] > CPU_THRESHOLD:
            send_alert_email("CPU Usage Alert", f"CPU usage is high: {metrics['cpu_usage']}%")
        if metrics["memory_usage"] > MEMORY_THRESHOLD:
            send_alert_email("Memory Usage Alert", f"Memory usage is high: {metrics['memory_usage']}%")
        if metrics["latency"] > LATENCY_THRESHOLD:
            send_alert_email("Network Latency Alert", f"Latency is high: {metrics['latency']} ms")
        if metrics["db_contention"] > 0:
            send_alert_email("Database Contention Alert", "Database contention detected!")
        if metrics["app_overhead"] > APP_OVERHEAD_THRESHOLD:
            send_alert_email("Application Layer Overhead Alert", f"App overhead is high: {metrics['app_overhead']} ms")

        # Sleep before checking again
        time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    monitor_system()
