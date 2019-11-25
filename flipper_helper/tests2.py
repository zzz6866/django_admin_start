from ctypes import *

libc = cdll.msvcrt
i = c_int()
f = c_float()
s = create_string_buffer(b'a' * 32)
print(i.value, ", ", f.value, ", ", repr(s.value))

libc.sscanf(b"1 3.14 Hello", b"%d %f %s", byref(i), byref(f), s)

print(i.value, ", ", f.value, ", ", repr(s.value))


a = (c_byte * 4)()
print(cast(a, POINTER(c_int)))
