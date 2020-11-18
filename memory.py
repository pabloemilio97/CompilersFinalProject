class SegmentBounds:
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

class Segment:
    """
    Chunk of memory allocated for each partition of our
    total memory. For example, we'll have an instance for global memory,
    another one for local memory, another one for temp memory.
    """
    int_index = 0
    float_index = 0
    char_index = 0
    int_chunk = {}
    float_chunk = {}
    char_chunk = {}

    index_assignments = {
        "int": int_index,
        "float": float_index,
        "char": char_index,
    }
    chunk_assignments = {
        "int": int_chunk,
        "float": float_chunk,
        "char": char_chunk,
    }

    def __init__(self, segment_bounds):
        self.segment_bounds = segment_bounds
        self.int_index = segment_bounds.INT_MIN
        self.float_index = segment_bounds.FLOAT_MIN
        self.char_index = segment_bounds.CHAR_MIN
    
    def push(self, type, value):
        """
        Add variable to memory, increment current index.
        Return assigned memory index.
        """
        index = self.index_assignments[type]
        chunk = self.chunk_assignments[type]
        chunk[index] = value
        self.index_assignments[type] += 1
        return index
    
    def get_value(self, index):
        """
        Get value from memory at the given index.
        """
        for chunk in self.chunk_assignments.values():
            try:
                return chunk[index]
            except KeyError:
                pass
        return None
    
    def flush(self):
        """
        Reset chunks and indexes.
        """
        self.int_index = self.segment_bounds.INT_MIN
        self.float_index = self.segment_bounds.FLOAT_MIN
        self.char_index = self.segment_bounds.CHAR_MIN
        self.int_chunk = {}
        self.float_chunk = {}
        self.char_chunk = {}

class Memory:
    global_memory = Segment(SegmentBounds(1000))
    local_memory = Segment(SegmentBounds(4000))
    tmp_memory = Segment(SegmentBounds(7000))
    constant_memory = Segment(SegmentBounds(10000))

memory = Memory()
    