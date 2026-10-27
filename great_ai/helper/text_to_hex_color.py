import colorsys
from hashlib import md5


def text_to_hex_color(text: str) -> str:
    encoded_text = text.encode("utf-8")

    digest = md5(
        encoded_text
    ).hexdigest()  # the built-in hash function is salted differently in each process

    integer = int(digest, 16)
    hue = integer % 6311 / 6311.0

    rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.6)

    return "#" + "".join("%02X" % round(i * 255) for i in rgb)
