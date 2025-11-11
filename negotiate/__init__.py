import logging
import azure.functions as func
from azure.messaging.webpubsubservice import WebPubSubServiceClient
import os
from dotenv import load_dotenv

load_dotenv()


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Negotiate function processed a request.')

    connection_string = os.environ['WebPubSubConnectionString']
    hub_name = 'chat'

    service_client = WebPubSubServiceClient.from_connection_string(
        connection_string,
        hub=hub_name
    )

    # Get user ID from query or use default
    user_id = req.params.get('userId', 'anonymous')

    # Generate client access token
    token = service_client.get_client_access_token(user_id=user_id)

    return func.HttpResponse(
        token['url'],
        status_code=200
    )
