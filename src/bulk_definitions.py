# Defaults for just about everything are 0
## Defaults are noted otherwis if they are different

ID_OFFSET = 11
BEAT_DIST = 144

# Logic Gates
## These are gates for nodes and node definitions
GATE_AND = 0
GATE_OR = 1
GATE_XOR = 2
GATE_BUF = 3
GATE_LED = 4

# Path Types
PATH_HTV = 0  # Horizontal then Vertical (default)
PATH_VTH = 1  # Vertical then Horizontal
PATH_STR = 2  # Straight

# Signal directions
SIG_SRR = 0  # Standard/Round Robit
SIG_ALL = 1  # All directions
SIG_RND = 2  # Random
SIG_NOW = 3  # Signal is instantaneous, also is sent in Round Robin style

TEMPLATE_TYPE_1 = {
    "force_scale": False,
    "probability": 100,
    "midi_data": {
        "Primary": 60,  # Note
        "Secondary": 100,  # Velocity
        "Channel": 1,
        "RawChannel": 0,  # Channel-1?
        "Duration": 1,
        "Repeat": 0,
        "Root": 0,
        "Scale": 0,
    },
    "relative_midi_data": {
        "Primary": 0,  # Note
        "RangedPrimary": 0,  # Note
        "Secondary": 0,  # Velocity
        "Channel": 0,
        "Duration": 0.0,
        "Repeat": 0,
        "Root": 0,
        "Scale": 0,
        "RangeFields": {
            "Primary": {"Up": False, "Down": False},
            "Secondary": {"Up": False, "Down": False},
            "Channel": {"Up": False, "Down": False},
            "Duration": {"Up": False, "Down": False},
            "Repeat": {"Up": False, "Down": False},
        },
        "Pass": {
            "Primary": False,
            "Secondary": False,
            "Channel": False,
            "Duration": False,
            "Repeat": False,
        },
    },
    "mute": False,
    "pass": False,
    "id": 0,
    "label": "",
    "color": {
        "B": 255,
        "G": 255,
        "R": 255,
        "A": 255,  # This may be unused
    },
    "group_data": {
        "Groups": [False, False, False, False, False, False, False, False, False, False]
    },
    "Start": False,
    "Origin": "0, 0",
    "PathMode": 0,
    "SignalMode": 0,
    "SerializablePathTo": [],
    "SerializablePathFrom": [],
    "SerializableLogicPathTo": [],
    "SerializableLogicPathFrom": [],
}

TEMPLATE_TYPE_3 = {
    "provision": 0,
    "negated": False,
    "send_color": False,
    "id": 0,
    "label": "",
    "color": {
        "B": 255,
        "G": 255,
        "R": 255,
        "A": 255,  # This may be unused
    },
    "group_data": {
        "Groups": [False, False, False, False, False, False, False, False, False, False]
    },
    "Gate": 0,
    "Origin": "0, 0",
    "PathMode": 0,
    "SignalMode": 0,
    "SerializablePathTo": [],
    "SerializablePathFrom": [],
    "SerializableLogicPathTo": [],
    "SerializableLogicPathFrom": [],
}

TEMPLATE_TYPE_5 = {
    "source_id": 0,
    "target_id": 0,
    "weight": 1,
    "logic": False,
    "Mode": 0,
}
