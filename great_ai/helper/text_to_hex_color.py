import colorsys
from hashlib import md5


def text_to_hex_color(text: str) -> str:
    ascii_bytes = text.encode("ascii")

    digest = md5(
        ascii_bytes
    ).hexdigest()  # the built-in hash function is salted differently in each process

    integer = int(digest, 16)
    hue = integer % 6311 / 6311.0

    rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.6)

    return "#" + "".join("%02X" % round(i * 255) for i in rgb)
