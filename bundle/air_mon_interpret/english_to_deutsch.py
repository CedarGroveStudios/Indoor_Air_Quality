# english_to_deutsch.py
# English to Deutsch (German)
# Thank you to @effiksmusic for the translation!

ENG_DEUTSCH = {
    "Air Quality": "Luftqualität",
    "ALARM": "ALARM",
    "Alarm": "Alarm",
    "CALIBRATE": "KALIBRIEREN",
    "DANGER": "GEFAHR",
    "ENGLISH": "DEUTSCH",
    "GOOD": "GUT",
    "HAZARDOUS": "GEFÄHRLICH",
    "Indoor Air Quality": "Raumluftqualität",
    "INVALID": "UNGÜLTIG",
    "LANGUAGE": "SPRACHE",
    "LOW BATTERY": "BATTERIE LEER",
    "MODERATE": "MÄSSIG",
    "OVERRANGE": "ÜBER MAXIMUM",
    "POOR": "SCHLECT",
    "SENSITIVE": "SENSIBEL",
    "TEMPERATURE": "TEMPERATUR",
    "UNHEALTHY": "UNGESUND",
    "V UNHEALTHY": "SEHR UNGESUND",
    "WARMUP": "VORBEREITUNG",
    "WARNING": "WARNUNG",
}


def interpret(enable, english_phrase):
    # returns translated phrase or original phrase
    if enable:
        if english_phrase in ENG_DEUTSCH:
            return ENG_DEUTSCH[english_phrase]
    return english_phrase
