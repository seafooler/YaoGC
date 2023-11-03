### Description
This repo implements the Yao's Garbled Circuit in Python, which mainly draws inspiration from n132's [repo](https://github.com/n132/SMC)

### Marks
1. The circuit defined in `equal.json` or `equal8.json` does not exactly describes a relationship of equation. Instead, it describes inequation. Accordingly, Line 54 in `Bob.py` expects the results with a `not` keyword. The reason for this is that the circuit to check the inequation between 2-bit values is simpler, as shown in `equal.json`.

### Requirement & Steps
Requirement: Python3

- Step 1 (execute the Bob.py): `python Bob.py`
- Step 2 (execute the Alice.py): `python Alice.py`