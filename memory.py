import error
import semantic_cube

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

    def __str__(self):
        s = ""
        s += f"int limits: {self.INT_MIN}, {self.INT_MAX}\n"
        s += f"float limits: {self.FLOAT_MIN}, {self.FLOAT_MAX}\n"
        s += f"char limits: {self.CHAR_MIN}, {self.CHAR_MAX}\n\n"
        return s


class Segment:
    """
    Chunk of memory allocated for each partition of our
    total memory. For example, we'll have an instance for global memory,
    another one for local memory, another one for temp memory.
    """
    def __init__(self, segment_bounds):
        self.segment_bounds = segment_bounds
        self.int_index = segment_bounds.INT_MIN
        self.float_index = segment_bounds.FLOAT_MIN
        self.char_index = segment_bounds.CHAR_MIN

        # Helps for determining in which chunk to push to
        self.chunks = {
            "int": {},
            "float": {},
            "char": {},
        }
    
    def _allocate_memory(self, type, space=1):
        if type == "int":
            self.int_index += space
            index = self.int_index - space
        elif type == "float":
            self.float_index += space
            index = self.float_index - space
        elif type == "char":
            self.char_index += space
            index = self.char_index - space
        else:
            raise TypeError

        return index

    def compile_push(self, type, dimensions=None):
        """
        Add variable to memory, increment current index.
        Return assigned memory index.
        """
        if dimensions is None:
            return self._allocate_memory(type)
        
        space = 1
        for d in dimensions:
            d = int(d)
            space *= d
        
        return self._allocate_memory(type, space)



    def get_value(self, index):
        """
        Get value from memory at the given index.
        """
        for chunk in self.chunks.values():
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
        self.chunks["int"] = {}
        self.chunks["float"] = {}
        self.chunks["char"] = {}
    
    def __str__(self):
        s = ""
        s += str(self.segment_bounds)
        for type, chunk in self.chunks.items():
            s += f"{type} chunk -> {str(chunk)}\n"
        return s

class Memory:
    # static variables, balonging to class and not to object
    global_memory = Segment(SegmentBounds(1000))
    local_memory = Segment(SegmentBounds(4000))
    tmp_memory = Segment(SegmentBounds(7000))
    tmp_pointer_memory = Segment(SegmentBounds(10000))
    constant_memory = Segment(SegmentBounds(13000))
    segments = [global_memory, local_memory, tmp_memory, constant_memory]

    def get_value(self, index):
        value = None
        for segment in self.segments:
            value = segment.get_value(index)
            if value is not None:
                return value
        error.gen_err(f"Índice de memoria {index} no encontrado.")
        return None

    # For debugging purposes
    def __str__(self):
        g = f"global_memory\n-------------------\n{self.global_memory}\n"
        l = f"local_memory\n-------------------\n{self.local_memory}\n"
        t = f"tmp_memory\n-------------------\n{self.tmp_memory}\n"
        c = f"constant_memory\n-------------------\n{self.constant_memory}\n"
        return f"{g}\n{l}\n{t}\n{c}"


memory = Memory()
    