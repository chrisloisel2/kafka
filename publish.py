import os
import json
import time
from kafka import KafkaProducer

KAFKA_BROKER      = os.environ.get("KAFKA_BROKER", "192.168.88.4")
KAFKA_BROKER_PORT = int(os.environ.get("KAFKA_BROKER_PORT", "9092"))
KAFKA_TOPIC       = os.environ.get("KAFKA_TOPIC", "topic2")

producer = KafkaProducer(
    bootstrap_servers=f"{KAFKA_BROKER}:{KAFKA_BROKER_PORT}",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

message = {
    "source": "pc",
    "pc_id": 1,
    "hostname": "PC-000040",
    "timestamp": "2026-03-07T11:21:06Z",
    "operator_username": "Jawad",
    "is_recording": False,
    "has_alert": False,
    "sqlite_queue": {
        "pending_sessions": 0,
        "total_records": 0,
        "oldest_pending_iso": None,
        "sessions": []
    },
    "last_send": {
        "session_id": "session_20260306_214748",
        "sent_at": "2026-03-06T21:47:57",
        "status": "failed",
        "records_sent": 0
    },
    "_sent_at": time.time()
}

t0 = time.time()
future = producer.send(KAFKA_TOPIC, value=message)
producer.flush()
record = future.get(timeout=10)
elapsed_ms = (time.time() - t0) * 1000

print(f"[OK] topic={record.topic}  partition={record.partition}  offset={record.offset}  latence={elapsed_ms:.1f}ms")
