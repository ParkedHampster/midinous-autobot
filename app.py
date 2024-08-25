# imports all constants and standard values
## wow this is kinda like C headers
from src.black_box import Midinous
# from src.bulk_definitions import *

shortterm = Midinous()
# shortterm.smush_gates = True
# shortterm.translate_image("ratm.jpg", dims=(40, 40), led_offset=(1440, 0))

shortterm.generate_animated_screen("skele.gif", dims=(20, 15))

shortterm.export("gif2")
