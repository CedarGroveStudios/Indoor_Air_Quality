# english_to_francais.py
# English to Français (French)
# Thank you to @DavidGlaude for the translation!

ENG_FRANCAIS = {
    "Air Quality": "Qualité de l'air",
    "ALARM": "ALARME",
    "Alarm": "Alarme",
    "CALIBRATE": "ÉTALONNAGE",
    "DANGER": "DANGER",
    "ENGLISH": "FRANÇAIS",
    "GOOD": "BON",
    "HAZARDOUS": "RISQUÉ",
    "Indoor Air Quality": "Qualité de l'air intérieur",
    "INVALID": "INVALIDE",
    "LANGUAGE": "LANGUE",
    "LOW BATTERY": "BATTERIE FAIBLE",
    "MODERATE": "MODÉRÉ",
    "OVERRANGE": "MAXIMUM",
    "POOR": "PAUVRES",
    "SENSITIVE": "SENSIBLE",
    "TEMPERATURE": "TEMPÉRATURE",
    "UNHEALTHY": "MALSAIN",
    "V UNHEALTHY": "TRÈS MALSAIN",
    "WARMUP": "PRÉCHAUFFE",
    "WARNING": "ATTENTION",
}


def interpret(enable, english_phrase):
    # returns translated phrase or original phrase
    if enable:
        if english_phrase in ENG_FRANCAIS:
            return ENG_FRANCAIS[english_phrase]
    return english_phrase
