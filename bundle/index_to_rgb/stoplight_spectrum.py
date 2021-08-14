# stoplight_spectrum.py
# 2021-08-11 version 1.0
# Copyright 2021 Cedar Grove Studios
# Spectral Index to Stop Light (Green-Yellow_Red) Spectrum RGB Converter Helper


def map_range(x, in_min, in_max, out_min, out_max):
    """
    Maps and constrains an input value from one range of values to another.
    (from adafruit_simpleio)
    :return: Returns value mapped to new range
    :rtype: float
    """
    in_range = in_max - in_min
    in_delta = x - in_min
    if in_range != 0:
        mapped = in_delta / in_range
    elif in_delta != 0:
        mapped = in_delta
    else:
        mapped = 0.5
    mapped *= out_max - out_min
    mapped += out_min
    if out_min <= out_max:
        return max(min(mapped, out_max), out_min)
    return min(max(mapped, out_max), out_min)


def index_to_rgb(index=0, gamma=0.5):
    """
    Converts a spectral index to "stop light" (green -> yellow -> red)
    spectrum to an RGB value. Spectral index in range of 0.0 to 1.0
    (green --> red). Gamma in range of 0.0 to 1.0 (1.0=linear),
    default 0.5 for color TFT displays.
    :return: Returns a 24-bit RGB value
    :rtype: integer
    """

    band = index * 600  # an arbitrary spectrum band index; 0 to 600

    if band >= 0 and band < 300:  # green to yellow
        red = map_range(band, 0, 300, 0.0, 1) ** gamma
        grn = map_range(band, 0, 300, 0.25, 1) ** gamma
        blu = 0.0
    if band >= 300:  # yellow to red
        red = 1.0 ** gamma
        grn = map_range(band, 300, 600, 1.0, 0.0) ** gamma
        blu = 0.0

    return (int(red * 255) << 16) + (int(grn * 255) << 8) + int(blu * 255)
