import numpy as np
import easygui
from life.grid_operations import insert_pattern_into_grid


def import_pattern(pattern_file, grid, grid_position=(1, 1)):
    pattern = import_rle(pattern_file)
    if pattern is not None:
        insert_pattern_into_grid(pattern, grid, grid_position)


def import_rle(rle_file):
    file = open(rle_file, "r")
    i, j = 0, 0
    # x, y = 0, 0
    digits = ""
    pattern = None
    try:
        for line in file:
            if line.startswith("#"):  # comment line
                continue
            elif line.lower().startswith("x"):  # size line
                xy_words = line.replace(" ", "").split("=")
                x = int(xy_words[1].split(",")[0])
                y = int(xy_words[2].split(",")[0])
                pattern = np.zeros((y, x), dtype=np.int32)
                continue
            parse_rle_line(pattern, line, i, j, digits)
    except Exception as e:
        easygui.msgbox("There was error during importing file:\n{}".format(e), "Error!")
    finally:
        file.close()
    return pattern


def parse_rle_line(pattern, line, i, j, digits):
    for char in line:
        if char == "$":  # next line
            i += 1
            j = 0
            digits = ""
        elif char == "!":  # end of rle file
            break
        elif char.isdigit():  # store number of cell occurrences
            digits += char
        elif char == "b":  # dead cell
            count = parse_rle_digits(digits)
            j += count
            digits = ""
        elif char == "o":  # live cell
            count = parse_rle_digits(digits)
            pattern[i, j: j + count] = 1
            j += count
            digits = ""


def parse_rle_digits(digits):
    if digits != "" and digits.isdigit():
        count = int(digits)
    else:
        count = 1
    return count