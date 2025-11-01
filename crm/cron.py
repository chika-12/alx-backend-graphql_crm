import logging
import requests
from datetime import datetime

logging.basicConfig(
  filename="/tmp/crm_heartbeat_log.txt",
  level=logging.INFO,
  format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_crm_heartbeat():
  url = "http://localhost:8000/graphql/"
  timestamp = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

  try:
    response = requests.get(url=url, )

    if response.status_code == 200:
      logging.info(f"{timestamp} CRM is alive")
    else:
      logging.warning(f"Heartbeat warning at {timestamp}. Status: {response.status_code}")
  except Exception as e:
    logging.error(f" Error: {e}")



