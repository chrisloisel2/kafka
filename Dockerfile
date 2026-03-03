FROM wurstmeister/kafka:latest

# Kafka est entièrement configuré via les variables d'environnement.
# Se référer au docker-compose.yml pour la configuration complète.
# Dépend de Zookeeper (voir Dockerfile.zookeeper).
#
# Ports :
#   9092 — listener INTERNAL (inter-conteneurs)
#   9093 — listener EXTERNAL (accès hôte, configurer SERVER_IP)
#
# Topics créés automatiquement : topic1 (20 partitions), topic2 (1 partition)
