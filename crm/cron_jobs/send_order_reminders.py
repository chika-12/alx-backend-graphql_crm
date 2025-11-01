from gql import gql, Client
from datetime import datetime
from gql.transport.requests import RequestsHTTPTransport
import logging


logging.basicConfig(
  filename="/tmp/order_reminders_log.txt",
  level=logging.INFO,                 # Log level (INFO or DEBUG)
  format="%(asctime)s - %(levelname)s - %(message)s"
)

try:

  transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
  )

  client = Client(transport=transport, fetch_schema_from_transport=True)
  query=gql("""
    {
      orders{
        id
        customer_id
        product_id
        order_data
      }
    }
  """
  )
  result = client.execute(query)

  logging.info(f"Query executed successfully. Result: {result}")
except Exception as e:
  logging.error(f"Error while executing GraphQL query: {e}")
