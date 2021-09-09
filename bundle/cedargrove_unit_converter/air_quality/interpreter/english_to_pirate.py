# english_to_pirate.py
# English to Pirate (Pirate)
ENG_PIRATE = {
    "Air Quality": "Crow's Nest Lookout",
    "ALARM": "BELLS",
    "Alarm": "Bells",
    "CALIBRATE": "BRING SPRING",
    "DANGER": "AVAST YE",
    "ENGLISH": "PIRATE",
    "GOOD": "SHIPSHAPE",
    "HAZARDOUS": "FEED FISH",
    "Indoor Air Quality": "Poop Deck Lookout",
    "INVALID": "SINK ME",
    "LANGUAGE": "AARRGGHH",
    "LOW BATTERY": "BLIMEY",
    "MODERATE": "THREE SHEETS",
    "OVERRANGE": "OVERBOARD",
    "POOR": "BATTEN YE",
    "SENSITIVE": "AVAST YE",
    "TEMPERATURE": "SWEATIN'",
    "UNHEALTHY": "YELLOW JACK",
    "V UNHEALTHY": "SHARK BAIT",
    "WARMUP": "FIRE IN HOLE",
    "WARNING": "BOW SHOT",
}


def interpret(enable, english_phrase):
    # returns translated phrase or original phrase
    if enable:
        if english_phrase in ENG_PIRATE:
            return ENG_PIRATE[english_phrase]
    return english_phrase
