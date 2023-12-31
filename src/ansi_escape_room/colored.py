#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
import sys

from .hex import HEX

TTY_AWARE = False
IS_TTY = sys.stdout.isatty() and sys.stderr.isatty()

_win_vterm_mode = None


# From:
#   https://github.com/ubernostrum/webcolors
def _hex_to_rgb(hex_value):
    """
    Convert a hexadecimal color value to a 3-tuple of integers
    suitable for use in an ``rgb()`` triplet specifying that color.
    """
    int_value = int(hex_value[1:], 16)
    return (int_value >> 16, int_value >> 8 & 0xFF, int_value & 0xFF)


def _rgb_to_hex(rgb_triplet, delim=""):
    """
    Convert a 3-tuple of integers, suitable for use in an ``rgb()``
    color triplet, to a normalized hexadecimal value for that color.
    """
    return "{:02x}{}{:02x}{}{:02x}".format(
        rgb_triplet[0],
        delim,
        rgb_triplet[1],
        delim,
        rgb_triplet[2],
    )


class colored(object):
    ESC = "\x1b["

    END = "m"

    PAINT = {
        "black": "0",
        "red": "1",
        "green": "2",
        "yellow": "3",
        "blue": "4",
        "magenta": "5",
        "cyan": "6",
        "light_gray": "7",
        "dark_gray": "8",
        "light_red": "9",
        "light_green": "10",
        "light_yellow": "11",
        "light_blue": "12",
        "light_magenta": "13",
        "light_cyan": "14",
        "white": "15",
        "grey_0": "16",
        "navy_blue": "17",
        "dark_blue": "18",
        "blue_3a": "19",
        "blue_3b": "20",
        "blue_1": "21",
        "dark_green": "22",
        "deep_sky_blue_4a": "23",
        "deep_sky_blue_4b": "24",
        "deep_sky_blue_4c": "25",
        "dodger_blue_3": "26",
        "dodger_blue_2": "27",
        "green_4": "28",
        "spring_green_4": "29",
        "turquoise_4": "30",
        "deep_sky_blue_3a": "31",
        "deep_sky_blue_3b": "32",
        "dodger_blue_1": "33",
        "green_3a": "34",
        "spring_green_3a": "35",
        "dark_cyan": "36",
        "light_sea_green": "37",
        "deep_sky_blue_2": "38",
        "deep_sky_blue_1": "39",
        "green_3b": "40",
        "spring_green_3b": "41",
        "spring_green_2a": "42",
        "cyan_3": "43",
        "dark_turquoise": "44",
        "turquoise_2": "45",
        "green_1": "46",
        "spring_green_2b": "47",
        "spring_green_1": "48",
        "medium_spring_green": "49",
        "cyan_2": "50",
        "cyan_1": "51",
        "dark_red_1": "52",
        "deep_pink_4a": "53",
        "purple_4a": "54",
        "purple_4b": "55",
        "purple_3": "56",
        "blue_violet": "57",
        "orange_4a": "58",
        "grey_37": "59",
        "medium_purple_4": "60",
        "slate_blue_3a": "61",
        "slate_blue_3b": "62",
        "royal_blue_1": "63",
        "chartreuse_4": "64",
        "dark_sea_green_4a": "65",
        "pale_turquoise_4": "66",
        "steel_blue": "67",
        "steel_blue_3": "68",
        "cornflower_blue": "69",
        "chartreuse_3a": "70",
        "dark_sea_green_4b": "71",
        "cadet_blue_2": "72",
        "cadet_blue_1": "73",
        "sky_blue_3": "74",
        "steel_blue_1a": "75",
        "chartreuse_3b": "76",
        "pale_green_3a": "77",
        "sea_green_3": "78",
        "aquamarine_3": "79",
        "medium_turquoise": "80",
        "steel_blue_1b": "81",
        "chartreuse_2a": "82",
        "sea_green_2": "83",
        "sea_green_1a": "84",
        "sea_green_1b": "85",
        "aquamarine_1a": "86",
        "dark_slate_gray_2": "87",
        "dark_red_2": "88",
        "deep_pink_4b": "89",
        "dark_magenta_1": "90",
        "dark_magenta_2": "91",
        "dark_violet_1a": "92",
        "purple_1a": "93",
        "orange_4b": "94",
        "light_pink_4": "95",
        "plum_4": "96",
        "medium_purple_3a": "97",
        "medium_purple_3b": "98",
        "slate_blue_1": "99",
        "yellow_4a": "100",
        "wheat_4": "101",
        "grey_53": "102",
        "light_slate_grey": "103",
        "medium_purple": "104",
        "light_slate_blue": "105",
        "yellow_4b": "106",
        "dark_olive_green_3a": "107",
        "dark_green_sea": "108",
        "light_sky_blue_3a": "109",
        "light_sky_blue_3b": "110",
        "sky_blue_2": "111",
        "chartreuse_2b": "112",
        "dark_olive_green_3b": "113",
        "pale_green_3b": "114",
        "dark_sea_green_3a": "115",
        "dark_slate_gray_3": "116",
        "sky_blue_1": "117",
        "chartreuse_1": "118",
        "light_green_2": "119",
        "light_green_3": "120",
        "pale_green_1a": "121",
        "aquamarine_1b": "122",
        "dark_slate_gray_1": "123",
        "red_3a": "124",
        "deep_pink_4c": "125",
        "medium_violet_red": "126",
        "magenta_3a": "127",
        "dark_violet_1b": "128",
        "purple_1b": "129",
        "dark_orange_3a": "130",
        "indian_red_1a": "131",
        "hot_pink_3a": "132",
        "medium_orchid_3": "133",
        "medium_orchid": "134",
        "medium_purple_2a": "135",
        "dark_goldenrod": "136",
        "light_salmon_3a": "137",
        "rosy_brown": "138",
        "grey_63": "139",
        "medium_purple_2b": "140",
        "medium_purple_1": "141",
        "gold_3a": "142",
        "dark_khaki": "143",
        "navajo_white_3": "144",
        "grey_69": "145",
        "light_steel_blue_3": "146",
        "light_steel_blue": "147",
        "yellow_3a": "148",
        "dark_olive_green_3": "149",
        "dark_sea_green_3b": "150",
        "dark_sea_green_2": "151",
        "light_cyan_3": "152",
        "light_sky_blue_1": "153",
        "green_yellow": "154",
        "dark_olive_green_2": "155",
        "pale_green_1b": "156",
        "dark_sea_green_5b": "157",
        "dark_sea_green_5a": "158",
        "pale_turquoise_1": "159",
        "red_3b": "160",
        "deep_pink_3a": "161",
        "deep_pink_3b": "162",
        "magenta_3b": "163",
        "magenta_3c": "164",
        "magenta_2a": "165",
        "dark_orange_3b": "166",
        "indian_red_1b": "167",
        "hot_pink_3b": "168",
        "hot_pink_2": "169",
        "orchid": "170",
        "medium_orchid_1a": "171",
        "orange_3": "172",
        "light_salmon_3b": "173",
        "light_pink_3": "174",
        "pink_3": "175",
        "plum_3": "176",
        "violet": "177",
        "gold_3b": "178",
        "light_goldenrod_3": "179",
        "tan": "180",
        "misty_rose_3": "181",
        "thistle_3": "182",
        "plum_2": "183",
        "yellow_3b": "184",
        "khaki_3": "185",
        "light_goldenrod_2a": "186",
        "light_yellow_3": "187",
        "grey_84": "188",
        "light_steel_blue_1": "189",
        "yellow_2": "190",
        "dark_olive_green_1a": "191",
        "dark_olive_green_1b": "192",
        "dark_sea_green_1": "193",
        "honeydew_2": "194",
        "light_cyan_1": "195",
        "red_1": "196",
        "deep_pink_2": "197",
        "deep_pink_1a": "198",
        "deep_pink_1b": "199",
        "magenta_2b": "200",
        "magenta_1": "201",
        "orange_red_1": "202",
        "indian_red_1c": "203",
        "indian_red_1d": "204",
        "hot_pink_1a": "205",
        "hot_pink_1b": "206",
        "medium_orchid_1b": "207",
        "dark_orange": "208",
        "salmon_1": "209",
        "light_coral": "210",
        "pale_violet_red_1": "211",
        "orchid_2": "212",
        "orchid_1": "213",
        "orange_1": "214",
        "sandy_brown": "215",
        "light_salmon_1": "216",
        "light_pink_1": "217",
        "pink_1": "218",
        "plum_1": "219",
        "gold_1": "220",
        "light_goldenrod_2b": "221",
        "light_goldenrod_2c": "222",
        "navajo_white_1": "223",
        "misty_rose1": "224",
        "thistle_1": "225",
        "yellow_1": "226",
        "light_goldenrod_1": "227",
        "khaki_1": "228",
        "wheat_1": "229",
        "cornsilk_1": "230",
        "grey_100": "231",
        "grey_3": "232",
        "grey_7": "233",
        "grey_11": "234",
        "grey_15": "235",
        "grey_19": "236",
        "grey_23": "237",
        "grey_27": "238",
        "grey_30": "239",
        "grey_35": "240",
        "grey_39": "241",
        "grey_42": "242",
        "grey_46": "243",
        "grey_50": "244",
        "grey_54": "245",
        "grey_58": "246",
        "grey_62": "247",
        "grey_66": "248",
        "grey_70": "249",
        "grey_74": "250",
        "grey_78": "251",
        "grey_82": "252",
        "grey_85": "253",
        "grey_89": "254",
        "grey_93": "255",
    }

    ATTRIBUTE = {
        "bold": ESC + "1" + END,
        1: ESC + "1" + END,
        "dim": ESC + "2" + END,
        2: ESC + "2" + END,
        "italic": ESC + "3" + END,
        3: ESC + "3" + END,
        "underlined": ESC + "4" + END,
        4: ESC + "4" + END,
        "blink": ESC + "5" + END,
        5: ESC + "5" + END,
        "reverse": ESC + "7" + END,
        7: ESC + "7" + END,
        "hidden": ESC + "8" + END,
        8: ESC + "8" + END,
        "reset": ESC + "0" + END,
        0: ESC + "0" + END,
        "res_bold": ESC + "21" + END,
        21: ESC + "21" + END,
        "res_dim": ESC + "22" + END,
        22: ESC + "22" + END,
        "res_italic": ESC + "23" + END,
        23: ESC + "23" + END,
        "res_underlined": ESC + "24" + END,
        24: ESC + "24" + END,
        "res_blink": ESC + "25" + END,
        25: ESC + "25" + END,
        "res_reverse": ESC + "27" + END,
        27: ESC + "27" + END,
        "res_hidden": ESC + "28" + END,
        28: ESC + "28" + END,
    }

    USE_TRUE_COLORS = True

    def __init__(self, color):
        self.color = color
        self.enable_windows_terminal_mode()
        self.HEX = ""
        self.RGB = ""
        if str(color).startswith("#"):
            if not colored.USE_TRUE_COLORS:
                # Convert #RRGGBB back to 0-255 ANSI color code (as string, not int).
                # This raises if value does not match basic 256 color (from the cube).
                self.HEX = HEX(color.lower())
            else:
                # (lb): In a tmux, with TERM=xterm, not all of the pre-canned ANSI
                # 256 colors render correctly -- some get "rounded" to the nearest
                # higher order color value. For example, on my machines, the
                # lightorange color, which you can test via:
                #     echo -e "\033[38;5;215m$(tput sgr0)" TEST
                # looks just like bold red, or:
                #     echo -e "\033[1m\033[31m$(tput sgr0)" TEST
                #     # Hrmm. tput-bold not bolding...
                #     #   echo -e "$(tput bold)\033[31m$(tput sgr0)" TEST
                # Fortunately, we can specify the RGB color instead of the
                # 0-255 ANSI code, at least for terminals that support TrueColor™.
                # This converts the #RRGGBB string value to an (r,g,b) int tuple.
                # REF: For list of 0-255 ANSI color codes and their RBG values, see:
                #   https://jonasjacek.github.io/colors/
                self.RGB = _hex_to_rgb(color)

    def attribute(self):
        """Set or reset attributes"""
        if TTY_AWARE and not IS_TTY:
            return ""
        return colored.ATTRIBUTE[self.color]

    def foreground(self):
        """Print 256 foreground colors"""
        if TTY_AWARE and not IS_TTY:
            return ""
        code = colored.ESC + "38;5;"
        if str(self.color).isdigit():
            self.reverse_dict()
            color = self.reserve_paint[str(self.color)]
            return code + colored.PAINT[color] + colored.END
        elif self.HEX:
            return code + str(self.HEX) + colored.END
        elif self.RGB:
            return "{}38;2;{};{};{}{}".format(
                colored.ESC, self.RGB[0], self.RGB[1], self.RGB[2], colored.END
            )
        else:
            return code + colored.PAINT[self.color] + colored.END

    def background(self):
        """Print 256 background colors"""
        if TTY_AWARE and not IS_TTY:
            return ""
        code = colored.ESC + "48;5;"
        if str(self.color).isdigit():
            self.reverse_dict()
            color = self.reserve_paint[str(self.color)]
            return code + colored.PAINT[color] + colored.END
        elif self.HEX:
            return code + str(self.HEX) + colored.END
        elif self.RGB:
            return "{}48;2;{};{};{}{}".format(
                colored.ESC, self.RGB[0], self.RGB[1], self.RGB[2], colored.END
            )
        else:
            return code + colored.PAINT[self.color] + colored.END

    def reverse_dict(self):
        """reverse dictionary"""
        self.reserve_paint = dict(zip(colored.PAINT.values(), colored.PAINT.keys()))

    def enable_windows_terminal_mode(self):
        """Enable virtual terminal processing in windows terminal. Does
        nothing if not on Windows. This is based on the rejected
        enhancement <https://bugs.python.org/issue29059>."""
        global _win_vterm_mode
        if _win_vterm_mode is not None:
            return _win_vterm_mode

        # Note: Cygwin should return something like "CYGWIN_NT..."
        _win_vterm_mode = platform.system().lower() == "windows"
        if _win_vterm_mode is False:
            return

        from ctypes import byref, c_int, c_void_p, windll

        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        INVALID_HANDLE_VALUE = c_void_p(-1).value
        STD_OUTPUT_HANDLE = c_int(-11)

        hStdout = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        if hStdout == INVALID_HANDLE_VALUE:
            _win_vterm_mode = False
            return

        mode = c_int(0)
        ok = windll.kernel32.GetConsoleMode(c_int(hStdout), byref(mode))
        if not ok:
            _win_vterm_mode = False
            return

        mode = c_int(mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
        ok = windll.kernel32.SetConsoleMode(c_int(hStdout), mode)
        if not ok:
            # Something went wrong, proably an too old version
            # that doesn't support the VT100 mode.
            # To be more certain we could check kernel32.GetLastError
            # for STATUS_INVALID_PARAMETER, but since we only enable
            # one flag we can be certain enough.
            _win_vterm_mode = False
            return


def attr(color):
    """alias for colored().attribute()"""
    return colored(color).attribute()


def fg(color):
    """alias for colored().foreground()"""
    return colored(color).foreground()


def bg(color):
    """alias for colored().background()"""
    return colored(color).background()


def stylize(text, styles, reset=True):
    """conveniently styles your text as and resets ANSI codes at its end."""
    terminator = attr("reset") if reset else ""
    return "{}{}{}".format("".join(styles), text, terminator)


def _c0wrap(styles):
    """wrap a set of ANSI styles in C0 control codes for readline safety."""
    C0_SOH = "\x01"  # mark the beginning of nonprinting characters
    C0_STX = "\x02"  # mark the end of nonprinting characters
    return "{}{}{}".format(C0_SOH, "".join(styles), C0_STX)


def stylize_interactive(text, styles, reset=True):
    """stylize() variant that adds C0 control codes (SOH/STX) for readline
    safety."""
    # problem: readline includes bare ANSI codes in width calculations.
    # solution: wrap nonprinting codes in SOH/STX when necessary.
    # see: https://gitlab.com/dslackw/colored/issues/5
    terminator = _c0wrap(attr("reset")) if reset else ""
    return "{}{}{}".format(_c0wrap(styles), text, terminator)


def set_tty_aware():
    """Makes all interactions here tty aware.  This means that if either
    stdout or stderr are directed to something other than a tty,
    colorization will not be added."""
    global TTY_AWARE
    TTY_AWARE = True
