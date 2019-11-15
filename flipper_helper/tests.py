from django.test import TestCase

# Create your tests here.

if __name__ == "__main__":
    import zugbruecke as ctypes

    simple_demo_routine = ctypes.windll.LoadLibrary('bin/wmca.dll')
    simple_demo_routine.wmcaIsConnected()
    # simple_demo_routine.argtypes = (ctypes.c_float, ctypes.c_float)
    # simple_demo_routine.restype = ctypes.c_float
    # return_value = simple_demo_routine(20.0, 1.07)
    # print('Got "%f".' % return_value)
