import logging
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
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
    query = gql("""
      {
        hello
      }
    """)
    transport = RequestsHTTPTransport(
      url=url,
      verify=True,
      retries=3
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)
    response = client.execute(query)
    if "hello" in response:
      logging.info(f"{timestamp} CRM is alive")
    else:
      logging.warning(f"{timestamp} CRM is not responding accordinly")
  except Exception as e:
    logging.error(f"Error: {e}")


