import numpy as np
from life.grid_operations import insert_pattern_into_grid


def import_pattern(pattern_file, grid, grid_position=(1, 1)):
    """
        Import pattern from ascii file and insert it into grid at specified position

        Parameters
        ----------
        pattern_file : str
            pattern file path
        grid : numpy.ndarray
            2 dimensional grid
        grid_position : tuple(int, int)
            grid index for insert pattern
    """
    pattern = import_rle(pattern_file)
    if pattern is not None:
        insert_pattern_into_grid(pattern, grid, grid_position)


def import_rle(rle_file):
    """
        Import pattern from RLE-file format

        Parameters
        ----------
        rle_file : str
            pattern RLE-file pattern

        Returns
        -------
        pattern : numpy.ndarray
            2 dimensional array
    """
    file = open(rle_file, "r")
    i, j = 0, 0
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
            (i, j) = parse_rle_line(pattern, line, (i, j), digits)
    except Exception as e:
        print("There was error during importing file:\n{}".format(e))

    finally:
        file.close()
    return pattern


def parse_rle_line(pattern, line, index, digits):
    """
        Parse line from RLE-file

        Parameters
        ----------
        pattern : numpy.ndarray
            2 dimensional array for storing pattern
        line : str
            line from RLE-file
        index : tuple(int, int)
            current (i - vertical, j - horizontal) index in pattern array
        digits : str
            string for dead/live cell counter in RLE-file
    """
    (i, j) = index
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
    return i, j


def parse_rle_digits(digits):
    """
        Helping function for 'parse_rle_line' function.
        Convert digits variable to integer

        Parameters
        ----------
        digits : str
            string for dead/live cell counter in RLE-file

        Returns
        -------
        count : int
            number of dead/live cells
    """
    if digits != "" and digits.isdigit():
        count = int(digits)
    else:
        count = 1
    return count
