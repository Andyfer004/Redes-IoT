# Lab 7 – IoT: Estación Meteorológica (Kafka)

Implementación del Laboratorio 7 de CC3067 Redes usando **Python** y **Apache Kafka**.

Se simula un nodo de estación meteorológica que envía lecturas de:
- Temperatura `[0, 110] °C`
- Humedad relativa `[0, 100] %`
- Dirección del viento `{N, NO, O, SO, S, SE, E, NE}`

Primero se envían en **JSON**, y luego en un **payload compacto de 3 bytes**.

---

## Requisitos

- Python 3.10+
- Acceso al broker Kafka del curso:

```text
Bootstrap server: iot.redesuvg.cloud:9092
Topic JSON:       22944
Topic compacto:   22944-compacto
```

> Los topics se pueden cambiar en los archivos .py si es necesario.

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Andyfer004/Redes-IoT.git
cd Redes-IoT
```

### 2. Crear y activar entorno virtual

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python3 -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Uso

### Modo 1: Mensajes JSON

**Producer (simulación de sensores)**

```bash
.venv/bin/python src/producer_json.py
```

- Genera temperatura, humedad y viento
- Envía un JSON al topic `22944` cada 15–30 segundos

**Consumer (gráfica en vivo)**

```bash
.venv/bin/python src/consumer_json.py
```

- Se suscribe al topic `22944`
- Deserializa el JSON y grafica temperatura y humedad con matplotlib

---

### Modo 2: Payload Compacto (3 bytes)

El payload empaqueta en 24 bits:
- **14 bits**: temperatura en centésimas (temp × 100, rango 0–11000)
- **7 bits**: humedad entera 0–100
- **3 bits**: dirección del viento (0–7)

La lógica de encode/decode está en `src/payload_codec.py`.

**Producer compacto**

```bash
.venv/bin/python src/producer_compacto.py
```

- Genera lecturas y las codifica a 3 bytes
- Envía los 3 bytes al topic `22944-compacto`

**Consumer compacto**

```bash
.venv/bin/python src/consumer_compacto.py
```

- Se suscribe al topic `22944-compacto`
- Decodifica los 3 bytes y grafica temperatura y humedad

---

## Estructura del Proyecto

```
slides/
  Lab7_Redes_IoT.pdf      # Reporte del laboratorio
src/
  producer_json.py        # Producer usando JSON
  consumer_json.py        # Consumer usando JSON + gráficas
  payload_codec.py        # Encode/Decode de payload de 3 bytes
  producer_compacto.py    # Producer usando payload compacto
  consumer_compacto.py    # Consumer para payload compacto
requirements.txt          # Dependencias (kafka-python, matplotlib, etc.)
README.md                 # Este archivo
```

---

## Notas

- Los scripts asumen que el broker Kafka del curso está disponible
- Para detener los producers/consumers, usar `Ctrl + C` en la terminal