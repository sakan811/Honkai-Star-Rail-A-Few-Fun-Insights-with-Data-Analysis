"""Version-related utility functions."""


def get_version_dict() -> dict[int, list[str]]:
    """
    Gets a dictionary of characters released in each version.
    
    Returns:
        Dictionary mapping version numbers to lists of character names.
    """
    return {
        1.1: ["luocha", "silver-wolf", "yukong"],
        1.2: ["blade", "kafka", "luka"],
        1.3: ["dan-heng-imbibitor-lunae", "fu-xuan", "lynx"],
        1.4: ["guinaifen", "topaz-&-numby", "jingliu"],
        1.5: ["argenti", "hanya", "huohuo"],
        1.6: ["dr-ratio", "ruan-mei", "xueyi"],
        2.0: ["black-swan", "misha", "sparkle"],
        2.1: ["acheron", "aventurine", "gallagher"],
        2.2: ["robin", "boothill", "trailblazer-the-harmony"],
        2.3: ["jade", "firefly"],
        2.4: ["yunli", "jiaoqiu", "march-7th-the-hunt"],
        2.5: ["feixiao", "lingsha", "moze"],
        2.6: ["rappa"],
        2.7: ["sunday", "fugue"],
        3.0: ["aglaea", "the-herta", "trailblazer-remembrance"],
        3.1: ["tribbie", "mydei"],
        3.2: ["anaxa", "castorice"],
        3.3: ["hyacine", "cipher"],
    } 