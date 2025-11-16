import random
import time
from kafka import KafkaProducer
from payload_codec import encode_payload

TOPIC = "22944"
BOOTSTRAP = "iot.redesuvg.cloud:9092"


def generar_medicion():
    temp = random.gauss(25, 5)
    temp = max(0, min(110, temp))

    hum = random.randint(0, 100)

    direcciones = ["N", "NO", "O", "SO", "S", "SE", "E", "NE"]
    viento = random.choice(direcciones)

    return temp, hum, viento


def main():
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP,
        key_serializer=lambda k: k.encode("utf-8"),
    )

    print("Producer compacto corriendo... Ctrl+C para salir")
    try:
        while True:
            temp, hum, viento = generar_medicion()
            payload = encode_payload(temp, hum, viento)
            print("Enviando (compacto):", temp, hum, viento, "->", payload)
            producer.send(TOPIC, key="sensor1", value=payload)
            producer.flush()
            time.sleep(random.randint(15, 30))
    except KeyboardInterrupt:
        print("\nSaliendo del producer compacto...")


if __name__ == "__main__":
    main()