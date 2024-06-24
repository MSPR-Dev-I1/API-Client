import os
from google.cloud.pubsub_v1 import PublisherClient
from app import schemas

google_project = os.getenv('GOOGLE_PROJECT')

def create_publisher(): # pragma: no cover
    """
        Créer un publisher
    """
    return PublisherClient()

def revoke_token_message(token_client: schemas.TokenClient):
    """"
        Publie un message sur le topic revoke-access-token-message-topic qui contient le token
    """
    publisher = create_publisher()
    revoke_token_topic_path = publisher.topic_path(
        google_project, 'revoke-access-token-message-topic')
    message = bytes(token_client.token, 'utf-8')
    publisher.publish(revoke_token_topic_path, message)
