from .spots import *

config = {
    "Silco": {
        "account": {
            "id": "Zaram",
            "pass": "***REMOVED***",
            "select_offset": 300
        },
        "stats": {
            "str": "f300",
            "agi": "r1",
            "vit": "f200",
            "ene": "r2",
        },
        "leveling_plan": [
            n_BUDGE_DRAGONS,
            n_WEREWOLVES,
            n_GRIZZLYS_2,
            n_GRIZZLYS_1,
            n_POISON_BULL_FIGHTERS_2,
            n_DARK_KNIGHTS_2,
            n_DARK_KNIGHTS_1
        ]
    },
    "Consumer": {
        "account": {
            "id": "Maraz",
            "pass": "***REMOVED***",
            "select_offset": 0
        },
        "stats": {
            "str": "r20",
            "agi": "r25",
            "vit": "f2500",
            "ene": "r30",
        },
        "leveling_plan": [
            n_BUDGE_DRAGONS,
            n_WEREWOLVES,
            n_POISON_BULL_FIGHTERS_1,
            n_DARK_KNIGHTS_2,
            n_DARK_KNIGHTS_1,
            n_THUNDER_LICHES_1,
            n_MUTANTS_2,
            n_MUTANTS_1,
            n_BLOODY_WOLVES_1,
            n_SPLINTER_WOLVES_3,
            n_SPLINTER_WOLVES_2,
            n_SPLINTER_WOLVES_1,
            # n_SAPI_UNUS1,
            # n_SAPI_DUOS1,
            # n_SAPI_DUOS2,
            n_BLADE_HUNTERS_2,
            n_BLADE_HUNTERS_1,
        ]
    }
}
