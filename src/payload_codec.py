DIRS = ["N", "NO", "O", "SO", "S", "SE", "E", "NE"]
dir_to_idx = {d: i for i, d in enumerate(DIRS)}


def encode_payload(temp_c, hum, wind_dir):
    temp_int = int(round(temp_c * 100))
    temp_int = max(0, min(11000, temp_int))

    hum = int(hum)
    hum = max(0, min(100, hum))

    w = dir_to_idx[wind_dir]  # 0..7

    # [ temp(14) | hum(7) | wind(3) ]
    packed = (temp_int << (7 + 3)) | (hum << 3) | w

    b0 = (packed >> 16) & 0xFF
    b1 = (packed >> 8) & 0xFF
    b2 = packed & 0xFF

    return bytes([b0, b1, b2])


def decode_payload(b):
    if len(b) != 3:
        raise ValueError("Payload debe tener 3 bytes")

    packed = (b[0] << 16) | (b[1] << 8) | b[2]

    w = packed & 0b111
    hum = (packed >> 3) & 0b1111111
    temp_int = (packed >> (7 + 3)) & ((1 << 14) - 1)
    temp_c = temp_int / 100.0

    return {
        "temperatura": temp_c,
        "humedad": hum,
        "direccion_viento": DIRS[w],
    }