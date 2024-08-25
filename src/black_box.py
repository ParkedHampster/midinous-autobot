import time
import json
import copy

from abc import ABC
from PIL import Image

# imports all of the constants that make this more legible
from .bulk_definitions import *

# This is present at the beginning of all files - seems to just define the version of Midinous
FILE_START = '{"Type":0,"JSON":"\\"1.2.0.0\\""}'
# This is present at the end of all files. Can be changed easily when you launch Midinous.
FILE_END = '{"Type":6,"JSON":"{\\"tempo\\":120.0,\\"grid_size\\":4,\\"beat_division\\":4,\\"beat_division_selector_index\\":1,\\"doc_scale\\":1,\\"scale_selector_index\\":0,\\"doc_root\\":1,\\"root_selector_index\\":0,\\"clock_source\\":2,\\"camera_position\\":\\"0, 0\\"}"}'


class Midinous(ABC):
    """
    A Midinous screen generator - maybe more will happen, who knows
    """

    def __init__(self):
        # unaccessed/unused - may be deleted {
        self.frame_w = 0
        self.frame_h = 0
        self.origin = [0, 0]
        self.n_leds = 0
        self.bit_depth = 6
        self.smush_gates = False
        self.origin_offset = {"x": 0, "y": 0}
        self.origin_mod = 1
        # }
        self.file_start = FILE_START
        self.file_end = FILE_END
        self.types = {"3": {}, "1": {}, "5": {}}
        self.node_ref = {}

    def export(self, title: str | None = None) -> None:
        """
        Write the defined object(s) to a Midinous-readable file
            Optionally pass in a pre-defined title
        """
        if type(title) is not str or len(title) == 0:
            timestamp = time.time()
            filename = f"midinous-autobot_{timestamp}.json"
        else:
            filename = f"{title}.json"
        with open(filename, "w") as f:
            f.write(f"{self.file_start}\n")
            for node_type, node_values in self.types.items():
                for _, item in node_values.items():
                    out_item = self.parse_dict(item, node_type)
                    f.write(f"{out_item}\n")
            f.write(self.file_end)

    def parse_dict(self, s: str, node_type: int | str = 3) -> str:
        """
        convert a dictionary into a JSON format that Midinous expects
        """
        defined_value = json.dumps(s).replace('"', '\\"')
        leader = '{"Type":' + str(node_type) + ',"JSON":"'
        output = f"{leader}{defined_value}\"{"}"}"
        return output

    def generate_locking_gate(
        self,
        isstart: bool = False,
        origin: tuple[float, float] = (0, 0),
    ) -> list:
        """
        Generate a standard locking gate
            TODO: All of it
                - killswitch y/n
                - map out with connections
        """
        """
        Dev Notes: 
        controller gate/switch is designed by default with this layout:
                    (buf)
                      v
                  ┌>(and)->(buf)
                (or )>┘
        if this is a starting point, it will include a muted starting note:
                    (c3x)
                      v
                    (buf)
                      v
                  ┌>(and)->(buf)
                (or )>┘
        """
        # hardcoded origins - FIX THIS
        buf_in = self.gen_logic(
            GATE_BUF,
            origin=(origin[0] + 0, origin[1] + 0),
            other_args=[("negated", True), ("PathMode", PATH_STR)],
        )
        and_control = self.gen_logic(
            GATE_AND,
            origin=(origin[0] + 4.501, origin[1] + 4.501),
            other_args=[("PathMode", PATH_STR)],
        )
        or_control = self.gen_logic(
            GATE_OR,
            origin=(origin[0] + 0.002, origin[1] + 4.502),
            other_args=[("PathMode", PATH_STR)],
        )
        buf_out = self.gen_logic(
            GATE_BUF,
            origin=(origin[0] + 4.503, origin[1] + 0.003),
            other_args=[("PathMode", PATH_STR)],
        )
        if isstart:
            start_note = self.gen_note(("mute", True))
            self.gen_path(start_note["id"], buf_in["id"])
        self.gen_path(buf_in["id"], and_control["id"], other_args=[("Mode", PATH_STR)])
        self.gen_path(
            or_control["id"], and_control["id"], other_args=[("Mode", PATH_STR)]
        )
        self.gen_path(
            and_control["id"], or_control["id"], other_args=[("Mode", PATH_STR)]
        )
        self.gen_path(and_control["id"], buf_out["id"], other_args=[("Mode", PATH_STR)])
        outputs = [buf_in, and_control, or_control, buf_out]
        return outputs

    def generate_led_pair(
        self,
        origin: tuple[float, float] = (0, 0),
        led_offset: tuple[float, float] = (0, 0),
        led_origin: tuple[float, float] | None = None,
    ) -> list:
        """
        Generate an LED with attached BUF nodes with color values
        Returns a list of the nodes
        """
        r1 = self.gen_logic(
            GATE_BUF,
            origin=(origin[0] + 0, origin[1] + 0.0),
            other_args=[
                (
                    "color",
                    {
                        "R": 127,
                        "G": 0,
                        "B": 0,
                    },
                ),
                ("send_color", True),
                ("PathMode", PATH_STR),
            ],
        )
        r2 = self.gen_logic(
            GATE_BUF,
            origin=(origin[0] + 0, origin[1] + 0.001),
            other_args=[
                (
                    "color",
                    {
                        "R": 127,
                        "G": 0,
                        "B": 0,
                    },
                ),
                ("send_color", True),
                ("PathMode", PATH_STR),
            ],
        )
        g1 = self.gen_logic(
            GATE_BUF,
            origin=(origin[0] + 0, origin[1] + 0.002),
            other_args=[
                (
                    "color",
                    {
                        "R": 0,
                        "G": 127,
                        "B": 0,
                    },
                ),
                ("send_color", True),
                ("PathMode", PATH_STR),
            ],
        )
        g2 = self.gen_logic(
            GATE_BUF,
            origin=(origin[0] + 0, origin[1] + 0.003),
            other_args=[
                (
                    "color",
                    {
                        "R": 0,
                        "G": 127,
                        "B": 0,
                    },
                ),
                ("send_color", True),
                ("PathMode", PATH_STR),
            ],
        )
        b1 = self.gen_logic(
            GATE_BUF,
            origin=(origin[0] + 0, origin[1] + 0.004),
            other_args=[
                (
                    "color",
                    {
                        "R": 0,
                        "G": 0,
                        "B": 127,
                    },
                ),
                ("send_color", True),
                ("PathMode", PATH_STR),
            ],
        )
        b2 = self.gen_logic(
            GATE_BUF,
            origin=(origin[0] + 0, origin[1] + 0.005),
            other_args=[
                (
                    "color",
                    {
                        "R": 0,
                        "G": 0,
                        "B": 127,
                    },
                ),
                ("send_color", True),
                ("PathMode", PATH_STR),
            ],
        )
        if led_origin is None:
            led_origin = led_offset[0] + origin[0] + 0, led_offset[1] + origin[1] + 144
        led = self.gen_logic(
            GATE_LED,
            origin=led_origin,
        )
        for c in [r1, r2, g1, g2, b1, b2]:
            self.gen_path(c["id"], led["id"], other_args=[("Mode", 2)])
        return []

    def generate_led_screen(
        self,
        width: int = 1,
        height: int = 1,
        led_distance: float = 72,
        led_offset: tuple[float, float] = (0, 1440),
    ) -> None:
        """
        Make a screen of width x height LEDs with a given distance between each LED of led_offset
        defaults to spreading out the LED and color nodes by 10 full beats (144 x 10)
        Currently no return - this may change?
        """
        for w in range(width):
            for h in range(height):
                print(w, h)
                # def generate_led_pair(self,origin:tuple[float,float]=(0,0),led_offset:tuple[float,float]=(0,0)) -> list:
                self.generate_led_pair(
                    origin=(w * 4.5, h * 4.5),
                    led_offset=led_offset,
                    led_origin=((w + 1) * led_distance, (h + 1) * led_distance),
                )

    def translate_image(
        self,
        im: str,
        dims: tuple[int, int] = (20, 10),
        led_scale: float = 72,
        led_offset: tuple[float, float] = (0, -1440),
    ) -> None:
        """
        Translates an image into a series of LED nodes in a given size (pending)
            TODO:
                add an origin parameter
                make it so that you can have multiple sets of color controllers to one screen (flipbook-ish)
        """
        img = Image.open(im)
        rs = img.resize(dims)
        rs.save(f"temp_out.{img.format}")
        cdata = list(rs.getdata())
        buf_list = []
        for h in range(rs.height):
            for w in range(rs.width):
                tmp_color = cdata.pop(0)
                rgb = {
                    "B": tmp_color[2],
                    "G": tmp_color[1],
                    "R": tmp_color[0],
                    "A": 255,
                }
                tmp_buf = self.gen_logic(
                    GATE_BUF,
                    origin=(w * 0.001, h * 0.001),
                    other_args=[("color", rgb), ("send_color", True)],
                )
                tmp_led = self.gen_logic(
                    GATE_LED,
                    origin=(
                        led_offset[0] + (w * led_scale),
                        led_offset[1] + (h * led_scale),
                    ),
                )
                buf_list.append(tmp_buf["id"])
                self.gen_path(tmp_buf["id"], tmp_led["id"])
        control_buf = self.gen_logic(
            GATE_BUF,
            origin=(led_offset[0] - led_scale, led_offset[1] - led_scale),
            other_args=[("negated", True)],
        )
        for buf_id in buf_list:
            self.gen_path(control_buf["id"], buf_id)

        return

    def generate_animated_screen(
        self,
        im: str | list[str],
        origin: tuple[float, float] = (0, 0),
        dims: tuple[int, int] = (20, 10),
        led_scale: float = 72,
        led_offset: tuple[float, float] = (0, -1440),
        controller_gap=36,
    ) -> None:
        if type(im) == list:
            print("Not yet implemented.")
            return
        buffered_images = []
        with Image.open(im) as anim:
            # This is the PIL recommended way to go through the
            try:
                while True:
                    buffered_image = anim.resize(dims).convert("RGB")
                    buffered_images.append(list(buffered_image.getdata()))
                    anim.seek(anim.tell() + 1)
            except EOFError:
                pass
        # Go through and generate a list of LEDs first - will need to go back
        ## through this to attach all of the conttrollers
        screen_matrix = []
        for h in range(dims[1]):
            screen_matrix.append([])
            for w in range(dims[0]):
                curr_led = self.gen_logic(
                    GATE_LED,
                    origin=(
                        origin[0] + led_offset[0] + led_scale * w,
                        origin[1] + led_offset[1] + led_scale * h,
                    ),
                )
                screen_matrix[h].append(curr_led["id"])
        for i, img in enumerate(buffered_images):
            buf_ids = []
            for h in range(dims[1]):
                for w in range(dims[0]):
                    cdata = img.pop(0)
                    rgb = {"R": cdata[0], "G": cdata[1], "B": cdata[2], "A": 255}
                    ctrl = self.gen_logic(
                        GATE_BUF,
                        origin=(w * 0.001, h * 0.001 + (i * controller_gap)),
                        other_args=[("color", rgb), ("send_color", True)],
                    )
                    self.gen_path(ctrl["id"], screen_matrix[h][w])
                    buf_ids.append(ctrl["id"])
            frame_ctrl = self.gen_logic(
                GATE_BUF,
                origin=(
                    led_offset[0] - led_scale,
                    led_offset[1] - led_scale - i * controller_gap,
                ),
                other_args=[("negated", True), ("label", f"Frame {i}")],
            )
            for buf_id in buf_ids:
                self.gen_path(frame_ctrl["id"], buf_id)
        return

    def gen_logic(
        self, gate: int = 0, other_args: None | list = None, origin: tuple = (0, 0)
    ) -> dict:
        """
        Generate a dict that describes a logic gate
            Type: 3
        """
        new_logic = copy.deepcopy(TEMPLATE_TYPE_3)
        id = len(self.node_ref) + ID_OFFSET
        new_logic["id"] = id
        new_logic["Gate"] = gate
        origin_str = f"{origin[0]}, {origin[1]}"
        new_logic["Origin"] = origin_str
        if other_args is not None:
            for arg in other_args:
                new_logic[arg[0]] = arg[1]
        self.types["3"][id] = new_logic
        self.node_ref[id] = "3"
        return new_logic

    def gen_note(self, *args) -> dict:
        """
        Generate a note object dict
            Type: 1
        """
        return {}

    def gen_path(
        self, from_node: int, to_node: int, other_args: list | None = None
    ) -> dict:
        """
        Generate a path dict
            Type: 5
        from_node: int
            the node id of the originator point
        to_node: int
            the node id of the destination point
        """
        id = len(self.node_ref) + ID_OFFSET
        self.node_ref[id] = "5"
        new_path = TEMPLATE_TYPE_5.copy()
        from_node_type = self.node_ref[from_node]
        to_node_type = self.node_ref[to_node]
        new_path["source_id"] = from_node
        new_path["target_id"] = to_node
        if other_args is not None:
            for arg in other_args:
                new_path[arg[0]] = arg[1]
        if from_node_type == "3" or to_node_type == "3":
            is_logic = "Logic"
            new_path["logic"] = True
        else:
            is_logic = ""
        dst_type = f"Serializable{is_logic}PathTo"
        tgt_type = f"Serializable{is_logic}PathFrom"

        #        new_path["id"] = id
        self.types["5"][id] = new_path
        self.types[from_node_type][from_node][dst_type].append(to_node)
        self.types[to_node_type][to_node][tgt_type].append(from_node)

        return new_path
