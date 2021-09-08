# english_to_francaise.py
# English to Française (French)

ENG_FRANCAISE = {
    "Air Quality": "Qualité de l'air",
    "ALARM": "ALARME",
    "Alarm": "Alarme",
    "CALIBRATE": "déterminer",
    "DANGER": "DANGER",
    "ENGLISH": "FRANÇAISE",
    "GOOD": "agréable",
    "HAZARDOUS": "HASARDEUX",
    "Indoor Air Quality": "Qualité de l'air intérieur",
    "INVALID": "INVALIDE",
    "LANGUAGE": "LANGUE",
    "LOW BATTERY": "BATTERIE FAIBLE",
    "MODERATE": "modéré",
    "OVERRANGE": "MAXIMUM",
    "POOR": "PAUVRES",
    "SENSITIVE": "SENSIBLE",
    "TEMPERATURE": "TEMPÉRATURE",
    "UNHEALTHY": "MALSAIN",
    "V UNHEALTHY": "TRÈS MALSAIN",
    "WARMUP": "PRÉPARATION",
    "WARNING": "précurseur",
}


def interpret(enable, english_phrase):
    # returns translated phrase or original phrase
    if enable:
        if english_phrase in ENG_FRANCAISE:
            return ENG_FRANCAISE[english_phrase]
    return english_phrase
