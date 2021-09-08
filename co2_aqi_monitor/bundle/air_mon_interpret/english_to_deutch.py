# english_to_deutch.py
# English to German

ENG_DEUTCH = {
    "Air Quality" : "Raumluftqualität",
    "ALARM"       : "ALARM",
    "Alarm"       : "Alarm",
    "CALIBRATE"   : "KALIBRIEREN",
    "DANGER"      : "GEFAHR",
    "ENGLISH"     : "DEUTCH",
    "GOOD"        : "GUT",
    "HAZARDOUS"   : "GEFÄHRLICH",
    "INVALID"     : "UNGÜLTIG",
    "LANGUAGE"    : "SPRACHE",
    "LOW BATTERY" : "NIEDRIGER BATTERIE",
    "MODERATE"    : "MÄSSIG",
    "OVERRANGE"   : "ÜBER MAXIMUM" ,
    "POOR"        : "SCHLECT",
    "SENSITIVE"   : "EMPFIDLICH",
    "TEMPERATURE" : "TEMPERATUR",
    "UNHEALTHY"   : "UNGESUND",
    "V UNHEALTHY" : "SEHR UNGESUND",
    "WARMUP"      : "ERWÄRMEN",
    "WARNING"     : "WARNUNG",
}

def interpret(enable, english_phrase):
    # returns translated phrase or original phrase
    if enable:
        if english_phrase in ENG_DEUTCH:
            return ENG_DEUTCH[english_phrase]
    return english_phrase
