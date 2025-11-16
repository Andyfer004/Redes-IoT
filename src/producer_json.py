import json
import random
import time
from kafka import KafkaProducer

TOPIC = "22944"  # tu carné
BOOTSTRAP = "iot.redesuvg.cloud:9092"


def generar_medicion():
    # Temperatura ~ gauss, recortada a [0, 110]
    temp = random.gauss(25, 5)
    temp = max(0, min(110, temp))

    # Humedad entera [0, 100]
    hum = random.randint(0, 100)

    # Dirección de viento
    direcciones = ["N", "NO", "O", "SO", "S", "SE", "E", "NE"]
    viento = random.choice(direcciones)

    return {
        "temperatura": round(temp, 2),
        "humedad": hum,
        "direccion_viento": viento,
    }


def main():
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8"),
    )

    print("Producer IoT corriendo... Ctrl+C para salir")
    try:
        while True:
            data = generar_medicion()
            print("Enviando:", data)
            producer.send(TOPIC, key="sensor1", value=data)
            producer.flush()
            time.sleep(random.randint(15, 30))
    except KeyboardInterrupt:
        print("\nSaliendo del producer...")


if __name__ == "__main__":
    main()