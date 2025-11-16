import json
from kafka import KafkaConsumer
import matplotlib.pyplot as plt

TOPIC = "22944"
BOOTSTRAP = "iot.redesuvg.cloud:9092"


def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP,
        group_id="22944-consumer-compacto",
        auto_offset_reset="latest",   # importante
        value_deserializer=lambda v: v,
    )



    temps, hums = [], []

    plt.ion()
    fig, ax1 = plt.subplots()

    for msg in consumer:
            payload = msg.value
            t = payload["temperatura"]
            h = payload["humedad"]

            temps.append(t)
            hums.append(h)

            # 👇 nos quedamos solo con las últimas 50 muestras
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