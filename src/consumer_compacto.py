from kafka import KafkaConsumer
import matplotlib.pyplot as plt
from payload_codec import decode_payload

TOPIC = "22944"
BOOTSTRAP = "iot.redesuvg.cloud:9092"


def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP,
        group_id="22944-consumer-compacto",
        auto_offset_reset="earliest",
        value_deserializer=lambda v: v,  # bytes crudos
    )

    temps, hums = [], []

    plt.ion()
    fig, ax1 = plt.subplots()

    for msg in consumer:
        payload_bytes = msg.value

        if len(payload_bytes) != 3:
            print("Ignorando mensaje no compacto, len =", len(payload_bytes))
            continue

        payload = decode_payload(payload_bytes)

        t = payload["temperatura"]
        h = payload["humedad"]

        temps.append(t)
        hums.append(h)

        temps = temps[-50:]
        hums = hums[-50:]

        ax1.clear()
        ax1.plot(temps, label="Temperatura (°C)")
        ax1.plot(hums, label="Humedad (%)")
        ax1.set_xlabel("Muestras")
        ax1.legend()
        ax1.grid(True)

        plt.draw()
        plt.pause(0.1)



if __name__ == "__main__":
    main()