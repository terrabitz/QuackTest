import pyautogui
import logging
import time
import string
import sys

single_char_list = list(string.printable)
special_key_dict = {
    "ENTER": "enter",
    "GUI": "win",
    "WINDOWS": "win",
    "MENU": "apps",
    "APP": "apps",
    "SHIFT": "shift",
    "ALT": "alt",
    "CONTROL": "ctrl",
    "CTRL": "ctrl",
    "DOWNARROW": "down",
    "DOWN": "down",
    "UPARROW": "up",
    "UP": "up",
    "LEFTARROW": "left",
    "LEFT": "left",
    "RIGHTARROW": "right",
    "BREAK": "right",
    "PAUSE": "pause",
    "CAPSLOCK": "capslock",
    "DELETE": "del",
    "END": "end",
    "ESC": "esc",
    "ESCAPE": "esc",
    "HOME": "home",
    "INSERT": "insert",
    "NUMLOCK": "numlock",
    "PAGEUP": "pageup",
    "PAGEDOWN": "pagedown",
    "PRINTSCREEN": "printscreen",
    "SCROLLLOCK": "scrolllock",
    "SPACE": " ",
    "TAB": "tab"
}


class QuackTester:
    def __init__(self, log_handler: logging.Handler = None):
        self.logger = logging.getLogger(__name__)
        stream_handler = logging.StreamHandler()
        self.logger.addHandler(stream_handler)
        if log_handler:
            self.logger.addHandler(log_handler)

        self.reset()

    def translate_key(self, key):
        key_upper = key.upper()
        if key_upper in special_key_dict.keys():
            return special_key_dict[key_upper]
        key_lower = key.lower()
        if key_lower in single_char_list:
            return key_lower
        raise ValueError("Key requested not valid: " + key)

    def press_multikeys(self, keys_to_press: list):
        self.logger.debug("Pressing the following keys: " + str(keys_to_press))
        normalized_keys_to_press = []
        for key in keys_to_press:
            normalized_keys_to_press.append(self.translate_key(key))
        for key in normalized_keys_to_press:
            pyautogui.keyDown(key)
        for key in normalized_keys_to_press:
            pyautogui.keyUp(key)

    def write_string(self, string_to_write):
        self.logger.debug("Received string command: " + string_to_write)
        pyautogui.typewrite(string_to_write)

    def delay(self, delay_time):
        self.logger.debug("Received delay:" + delay_time)
        try:
            time_to_delay = int(delay_time) / 1000
            return time_to_delay
        except ValueError as e:
            raise ValueError("DELAY command run with " + delay_time + " as argument")

    def replay(self, replay_num):
        try:
            replay_num_int = int(replay_num)
            for i in range(replay_num_int):
                self.interpret_line(self.last_line)
        except ValueError as e:
            raise ValueError("REPLAY command run with " + replay_num + " as argument")

    def rem(self, comment):
        self.logger.debug("Received comment: " + comment)

    def interpret_line(self, line):
        # logger.debug("Interpreting line: " + line)
        if not line:
            return

        time.sleep(self.current_default_delay)

        split_line = line.split(maxsplit=1)
        command = split_line[0]
        remainder = ""
        if len(split_line) > 1:
            remainder = split_line[1]

        command = command.upper()
        if command == "REM":
            self.rem(remainder)
        elif command == "STRING":
            self.write_string(remainder)
        elif command == "DELAY":
            time_to_delay = self.delay(remainder)
            time.sleep(time_to_delay)
        elif command == "DEFAULT_DELAY" or command == "DEFAULTDELAY":
            time_to_delay = self.delay(remainder)
            self.current_default_delay = time_to_delay
        elif command == "REPLAY":
            self.replay(remainder)
        else:
            self.press_multikeys(line.split())

        self.last_line = line

    def run(self, script: list, soft_errors=True, log_level=logging.INFO):
        '''
        Runs the provided script

        :param script: A list of lines containing the Ducky script being used
        :param soft_errors: Determines whether the program should quit on errors
        or continue executing the remainder of the script
        '''
        self.logger.setLevel(log_level)
        self.reset()

        for index, line in enumerate(script):
            try:
                self.interpret_line(line.strip())
            except Exception as e:
                self.logger.error("Error found at line " + str(index) + ": " + str(e))
                if soft_errors:
                    pass
                else:
                    self.logger.error("Exiting...")
                    sys.exit(1)

    def reset(self):
        self.current_default_delay = 0
        self.last_line = ""
