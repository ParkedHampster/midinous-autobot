# General

## Overview

This file is incomplete.

There are notes on the schemas and types of nodes and gates insofar as what I have personally found.  
Not everything has been tested completely, and not all pieces are fully confirmed across the board.

Any notes I have taken that are specific (e.g. what numbers each GATE are) _HAVE_ been confirmed.

## Notes

smallest steps are 4.5 units apart (in 4/4 when snapping to grid)
smallest steps are 3 when using a triplet grid
steps as low as 0.001 can be defined and in this case the nodes are directly on top of one another essentially
newlines can be defined in JSON but seemingly not in the UI

1 quarter note (in 4/4) is 144 units in a given direction

it looks like the minimum ID for a node is 11 (?)

### TOC

1. [Schemas and Definitions](#schemas-and-definitions)
   - [Types](#types)
1. [Required/Existing Items (Per Type)](#requiredexisting-items-per-type)

## Schemas and Definitions

### Types

0. Header data - must be present and only once at the top
   - `{"Type":0, "JSON":"\"1.2.0.0\""}`
1. MIDI/Note data
2. ? (maybe CC?)
3. Logic
4. ????
5. Connection (logical and note-ical)
6. Music metadata - tempo, divisions, size, etc. and Camera Position

All types have a "JSON" field as their first field - this is being omitted

## Required/Existing Items (Per Type)

File order for types is 0, 3, 1, 5, 6 (unsure where 2 is)

### Type 1

MIDI notes

```JSON
{"Type":1,"JSON":"{\"force_scale\":false,\"probability\":100,\"midi_data\":{\"Primary\":60,\"Secondary\":100,\"Channel\":1,\"RawChannel\":0,\"Duration\":1.0,\"Repeat\":0,\"Root\":0,\"Scale\":0},\"relative_midi_data\":{\"Primary\":0,\"RangedPrimary\":0,\"Secondary\":0,\"Channel\":0,\"Duration\":0.0,\"Repeat\":0,\"Root\":0,\"Scale\":0,\"RangeFields\":{\"Primary\":{\"Up\":false,\"Down\":false},\"Secondary\":{\"Up\":false,\"Down\":false},\"Channel\":{\"Up\":false,\"Down\":false},\"Duration\":{\"Up\":false,\"Down\":false},\"Repeat\":{\"Up\":false,\"Down\":false}},\"Pass\":{\"Primary\":false,\"Secondary\":false,\"Channel\":false,\"Duration\":false,\"Repeat\":false}},\"mute\":false,\"pass\":false,\"id\":8,\"label\":\"\",\"color\":{\"B\":255,\"G\":255,\"R\":255,\"A\":255},\"group_data\":{\"Groups\":[false,false,false,false,false,false,false,false,false,false]},\"Start\":false,\"Origin\":\"-4.5, 4.5\",\"PathMode\":0,\"SignalMode\":0,\"SerializablePathTo\":[],\"SerializablePathFrom\":[],\"SerializableLogicPathTo\":[],\"SerializableLogicPathFrom\":[]}"}
```

- force_scale -> bool
- probability
- midi_data -> dict
  - Primary -> int
  - Secondary
  - Channel
  - RawChannel
  - Duration
  - Repeat
  - Root
  - Scale
- relative_midi_data
  - Primary
  - RangedPrimary
  - Secondary
  - Channel
  - Duration
  - Repeat
  - Root
  - Scale
  - RangeFields
    - Primary
      - Up/Down
    - Secondary
    - Channel
    - Duration
    - Repeat
  - Pass
    - Primary
    - Secondary
    - Channel
    - Duration
    - Repeat
- mute
- pass
- id
- label
- color
  - B
  - G
  - R
  - A
    - this seems to be unused
- group_data
  - Groups
    - this is an array of control groups, all T/F for each group 1-10 (0-9)
- Start
- Origin -> str\*
  - comma-separated string consisting of 2 integers
- PathMode -> int
  - Values:
    - Standard/Horiz. then Vert.: 0
    - Vert then Horiz: 1
    - Straight Line: 2
- SignalMode -> int
  - Values:
    - Standard/RR: 0
    - Every Direction: 1
    - Random Direction: 2
    - Instant: 3
- SerializablePathTo -> list[int]
- SerializablePathFrom -> list[int]
- SerializableLogicPathTo -> list[int]
- SerializableLogicPathFrom -> list[int]
  - Serializable... are all list of integer IDs for the next node in the connection.
  - I have no idea why this field exists when the path entries also exist.

### Type 2

???

### Type 3

Logic - this is where everything meaty is going to go
ex:

```JSON
{"Type":3,"JSON":"{\"provision\":0,\"negated\":true,\"send_color\":false,\"id\":3,\"label\":\"\",\"color\":{\"B\":255,\"G\":255,\"R\":255,\"A\":255},\"group_data\":{\"Groups\":[false,false,false,false,false,false,false,false,false,false]},\"Gate\":0,\"Origin\":\"13.5, -9\",\"PathMode\":0,\"SignalMode\":0,\"SerializablePathTo\":[],\"SerializablePathFrom\":[],\"SerializableLogicPathTo\":[1],\"SerializableLogicPathFrom\":[]}"}
```

- provision -> int (?)
- negated -> bool
- send_color -> bool
- id -> int
- label -> str
- color -> dict
  - B -> int
  - G -> int
  - R -> int
  - A -> int
    - may be unused
- group_data -> dict
  - Groups -> list[bool*10]
- Gate -> int
  - Values:
    - AND:0
    - OR: 1
    - XOR: 2
    - BUF: 3
    - LED: 4
- Origin -> str\*
  - string is two floats sepated by a comma and space. (e.g. "0, 4.5")
- PathMode -> int
- SignalMode -> int
- SerializablePathTo -> list[int]
- SerializablePathFrom -> list[int]
- SerializableLogicPathTo -> list[int]
- SerializableLogicPathFrom -> list[int]
  - Serializable... are all list of integer IDs for the next node in the connection.
  - I have no idea why this field exists when the path entries also exist.

### Type 5

Dictates paths, both logical and noteical
**_Must_** match what is present in the nodes' serializable path lists.

```JSON
{"Type":5,"JSON":"{\"source_id\":11,\"target_id\":12,\"weight\":1,\"logic\":true,\"Mode\":0}"}
```

- source_id -> int
- target_id -> int
- weight -> int
- logic -> bool
- Mode -> int: ?

---

## What Makes a Controller?

each logic gate has:

- An input (one is a !BUF or !XOR for the first one)
- an OR that has an input and output to the AND
- a BUF that connects to the next item (in a counter/adding system)
