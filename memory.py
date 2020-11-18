class Segment:
    INT_MIN = 0
    INT_MAX = 999
    FLOAT_MIN = 1000
    FLOAT_MAX = 1999
    CHAR_MIN = 2000
    CHAR_MAX = 2999

    def __init__(self, base_dir):
        self.INT_MIN += base_dir
        self.INT_MAX += base_dir
        self.FLOAT_MIN += base_dir
        self.FLOAT_MAX += base_dir
        self.CHAR_MIN += base_dir
        self.CHAR_MAX += base_dir


# global variables
global_dir = Segment(1000)

# local variables
local_dir = Segment(4000)

# temporal variables
tmp_dir = Segment(7000)

# constant variables
constant_dir = Segment(10000)