import os

REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT: int = int(os.getenv('REDIS_PORT', 6379))

MQTT_HOST: str = os.getenv('MQTT_HOST', 'af120153-db6a-4fdd-a81b-6d902b00e936.nodes.k8s.fr-par.scw.cloud')
MQTT_PORT: int = int(os.getenv('MQTT_PORT', 32500))

# SPRINKLERS TOPICS
# Sprinkler node
MQTT_REGISTRY_TOPIC: str = f'sprinkler/config/registry'
MQTT_REGISTRY_VALIDATION_TOPIC_TEMPLATE: str = 'sprinkler/config/registry/validation/{tag}'
