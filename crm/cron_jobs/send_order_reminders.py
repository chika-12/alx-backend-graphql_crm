#!/usr/bin/env python3
import requests
from datetime import datetime
import os
url = "http://localhost:8000/graphql/"
timestamp = timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
log_dir = os.path.join(BASE_DIR, 'tmp')
log_file = os.path.join(log_dir, 'order_reminder_log.txt')
# Ensure the tmp directory exists
os.makedirs(log_dir, exist_ok=True)
query = """
query{
  orders(status:pending){
    id
    customer_id
    product_id
    order_data
  }
}
"""
headers = {
  "Content-Type": "apllication/json" 
}
response = requests.post(url, json={'query':query}, headers=headers)
with open(log_file, "a") as file:
  file.write(f"[{timestamp}] Status code {response.status_code}\n")
  file.write(response.text +  "\n\n")
print("Order reminders processed!")