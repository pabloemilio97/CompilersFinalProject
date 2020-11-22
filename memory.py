import error
import semantic_cube
import math

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
    
    def _get_address_type(self, address):
        bounds = self.segment_bounds
        if bounds.INT_MIN <= address <= bounds.INT_MAX:
            return "int"
        elif bounds.FLOAT_MIN <= address <= bounds.FLOAT_MAX:
            return "float"
        elif bounds.CHAR_MIN <= address <= bounds.CHAR_MAX:
            return "char"
        error.gen_err(f"Dirección de memoria {address} fuera de rango.")

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


    def get_value(self, address):
        """
        Get value from memory at the given address.
        """
        for chunk in self.chunks.values():
            try:
                return chunk[address]
            except KeyError:
                pass
        return None
    
    def assign_value(self, address, value):
        """
        Assign value at given memory address.
        """
        type = self._get_address_type(address)
        chunk = self.chunks[type]
        chunk[address] = value


    
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

class VirtualMemory:
    # static variables, balonging to class and not to object
    global_memory = Segment(SegmentBounds(1000))
    constant_memory = Segment(SegmentBounds(13000))
    
    def __init__(self):
        self.local_memory = Segment(SegmentBounds(4000))
        self.tmp_memory = Segment(SegmentBounds(7000))
        self.tmp_pointer_memory = Segment(SegmentBounds(10000))

        self.address_memory = {
            (1000, 4000): self.global_memory,
            (4000, 7000): self.local_memory,
            (7000, 10000): self.tmp_memory,
            (10000, 13000): self.tmp_pointer_memory,
            (13000, math.inf): self.constant_memory,
        }

    def _get_segment(self, address):
        segment = None
        for lower, upper in self.address_memory:
            if lower <= address < upper:
                segment = self.address_memory[(lower, upper)]
                return segment
        error.gen_err(f"Dirección de memoria incorrecta '{address}'.")

    def get_value(self, index):
        # Is a pointer
        if isinstance(index, str):
            index = int(index[1:-1])
            value = self.tmp_pointer_memory.get_value(index)
            value = self.tmp_pointer_memory.get_value(value)
            return value
        value = None
        for segment in list(self.address_memory.values()):
            value = segment.get_value(index)
            if value is not None:
                return value
        error.gen_err(f"Índice de memoria {index} no encontrado.")
        return None

    def assign_value(self, address, value):
        segment = self._get_segment(address)
        segment.assign_value(address, value)
 
    # For debugging purposes
    def __str__(self):
        g = f"global_memory\n-------------------\n{self.global_memory}\n"
        l = f"local_memory\n-------------------\n{self.local_memory}\n"
        t = f"tmp_memory\n-------------------\n{self.tmp_memory}\n"
        c = f"constant_memory\n-------------------\n{self.constant_memory}\n"
        return f"{g}\n{l}\n{t}\n{c}"

class CompilationMemory:
    # static variables, balonging to class and not to object
    global_memory = Segment(SegmentBounds(1000))
    local_memory = Segment(SegmentBounds(4000))
    tmp_memory = Segment(SegmentBounds(7000))
    tmp_pointer_memory = Segment(SegmentBounds(10000))
    constant_memory = Segment(SegmentBounds(13000))
    segments = [global_memory, local_memory, tmp_memory, constant_memory]


    def get_address_type(self, address):
        for segment in self.segments:
            bounds = segment.segment_bounds
            if bounds.INT_MIN <= address <= bounds.INT_MAX:
                return "int"
            elif bounds.FLOAT_MIN <= address <= bounds.FLOAT_MAX:
                return "float"
            elif bounds.CHAR_MIN <= address <= bounds.CHAR_MAX:
                return "char"
        error.gen_err(f"Dirección de memoria {address} fuera de rango.")

    # For debugging purposes
    def __str__(self):
        g = f"global_memory\n-------------------\n{self.global_memory}\n"
        l = f"local_memory\n-------------------\n{self.local_memory}\n"
        t = f"tmp_memory\n-------------------\n{self.tmp_memory}\n"
        c = f"constant_memory\n-------------------\n{self.constant_memory}\n"
        return f"{g}\n{l}\n{t}\n{c}"


compilation_mem = CompilationMemory()
    
