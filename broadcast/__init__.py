import logging
import azure.functions as func
from azure.messaging.webpubsubservice import WebPubSubServiceClient
import os
import json
from dotenv import load_dotenv

load_dotenv()


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Broadcast function processed a request.')

    connection_string = os.environ['WebPubSubConnectionString']
    hub_name = 'chat'

    service_client = WebPubSubServiceClient.from_connection_string(
        connection_string,
        hub=hub_name
    )

    try:
        req_body = req.get_json()
        message = req_body.get('message')

        # Broadcast to all clients
        service_client.send_to_all({
            'type': 'message',
            'data': message
        })

        return func.HttpResponse(
            json.dumps({'status': 'Message sent'}),
            status_code=200,
            mimetype='application/json'
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({'error': str(e)}),
            status_code=400,
            mimetype='application/json'
        )
