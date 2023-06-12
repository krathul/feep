from pynput.keyboard import Key

KEYS_NAMES = [ key.name for key in Key]
KEYS_MAP = {key.name: Key[key.name] for key in Key}

OPTIMIZED_KEYS_MAP = {
    "backspace": "bs",
    "tab": "tb",
    "enter": "en",
    "shift": "sh",
    "shift_r": "sh_r",
    "cmd": "cm",
    "cmd_r": "cm_r",
    "ctrl": "ct",
    "ctrl_r": "ct_r",
    "alt": "al",
    "alt_r": "al_r",
    "alt_gr": "al_gr",
    "pause": "pa",
    "caps_lock": "cl",
    "esc": "es",
    "space": "sp",
    "page_up": "pu",
    "page_down": "pd",
    "end": "ed",
    "home": "hm",
    "left": "lf",
    "up": "up",
    "right": "rt",
    "down": "dn",
    "print_screen": "ps",
    "insert": "is",
    "delete": "dl",
    "num_lock": "nl",
    "scroll_lock": "sl",
    "f1": "f1",
    "f2": "f2",
    "f3": "f3",
    "f4": "f4",
    "f5": "f5",
    "f6": "f6",
    "f7": "f7",
    "f8": "f8",
    "f9": "f9",
    "f10": "f10",
    "f11": "f11",
    "f12": "f12",
    "f13": "f13",
    "f14": "f14",
    "f15": "f15",
    "f16": "f16",
    "f17": "f17",
    "f18": "f18",
    "f19": "f19",
    "f20": "f20",
    "media_play_pause": "mp",
    "media_volume_mute": "mv",
    "media_volume_down": "md",
    "media_volume_up": "mu",
    "media_next": "mn",
    "media_previous": "mr",
    "menu": "me",
}

def __validateKeys():
    for key in KEYS_NAMES:
        if key not in OPTIMIZED_KEYS_MAP:
            print("------------- Invalid key, remove it: " + key)

    for key in OPTIMIZED_KEYS_MAP:
        if key not in KEYS_NAMES:
            print("++++++++++++++ Missing key, add it: " + key)

__validateKeys()
