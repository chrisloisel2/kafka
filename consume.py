import os
import json
import time
from kafka import KafkaConsumer

KAFKA_BROKER      = os.environ.get("KAFKA_BROKER", "192.168.88.4")
KAFKA_BROKER_PORT = int(os.environ.get("KAFKA_BROKER_PORT", "9092"))
KAFKA_TOPIC       = os.environ.get("KAFKA_TOPIC", "monitoring")
HOSTNAME_FILTER   = os.environ.get("HOSTNAME_FILTER", "")

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=f"{KAFKA_BROKER}:{KAFKA_BROKER_PORT}",
    auto_offset_reset="latest",   # ne rejoue pas l'historique
    enable_auto_commit=True,
    group_id=None,  # pas de groupe = toujours latest, sans offset persisté
    value_deserializer=lambda v: v  # décodage brut, parsing dans la boucle
)

print(f"[consumer] en attente sur {KAFKA_TOPIC} @ {KAFKA_BROKER}:{KAFKA_BROKER_PORT} ...")

for message in consumer:
    try:
        data = json.loads(message.value.decode("utf-8")) if message.value else None
    except (json.JSONDecodeError, UnicodeDecodeError):
        continue
    if not data:
        continue

    hostname = data.get("hostname", "")
    if HOSTNAME_FILTER and hostname != HOSTNAME_FILTER:
        continue

    sent_at = data.pop("_sent_at", None)
    latency = f"  latence={((time.time() - sent_at) * 1000):.1f}ms" if sent_at else ""

    print(f"[recu] partition={message.partition} offset={message.offset} hostname={hostname}{latency}")
    print(json.dumps(data, indent=2))
