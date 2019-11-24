import ctypes

""""
#include <stdio.h>

typedef enum {
    VP_NONE,
    VP_INT,
    VP_DOUBLE,
    VP_CHAR
} vptype;

int vpfunc(int type, void *vp, int nele)
{
    int i;
    int *ip = NULL;
    double *dp = NULL;
    char **cp = NULL;

    printf("C: vpfunc(%d, <%016lx>, %d)\n", type, (long unsigned int)vp, nele);
    switch(type) {
    case VP_INT:
        printf("INT array is passed...\n");
        ip = (int *)vp;
        for (i = 0; i < nele; ++i) {
            printf("\t[%d] %d\n", i, ip[i]);
        }
        break;
    case VP_DOUBLE:
        printf("DOUBLE array is passed...\n");
        dp = (double *)vp;
        for (i = 0; i < nele; ++i) {
            printf("\t[%d] %f\n", i, dp[i]);
        }
        break;
    case VP_CHAR:
        printf("CHAR array is passed...\n");
        cp = (char **)vp;
        for (i = 0; i < nele; ++i) {
            printf("\t[%d] '%s'\n", i, cp[i]);
        }
        break;
    default:
        printf("Invalid type <%d>\n", type);
    }
    return (int)type;
}
"""


class VP:
    # =====================================================================================
    VP_NONE = 0
    VP_INT = 1
    VP_DOUBLE = 2
    VP_CHAR = 3
    # =====================================================================================
    sofile = './libvp.so'
    clib = ctypes.CDLL(sofile)
    # int vpfunc(int type, void *vp, int nele)
    clib.vpfunc.argtypes = (ctypes.c_int, ctypes.c_void_p, ctypes.c_int)
    clib.vpfunc.restype = ctypes.c_int

    # =====================================================================================
    def call_vpfunc(self, vplist):
        if not isinstance(vplist, (list, tuple)):
            raise RuntimeError("Only list (or tuple) is needed!")
        if not vplist:
            raise ReferenceError("Empty list(or tuple) is not allowed!")
        nele = len(vplist)
        vptype = self.VP_NONE
        if isinstance(vplist[0], int):
            packed_data = (ctypes.c_int * nele)(*vplist)
            vptype = self.VP_INT
        elif isinstance(vplist[0], float):
            packed_data = (ctypes.c_double * nele)(*vplist)
            vptype = self.VP_DOUBLE
        elif isinstance(vplist[0], str):
            packed_data = (ctypes.c_char_p * nele)(*vplist)
            vptype = self.VP_CHAR
        else:
            raise RuntimeError("Invalid type")
        pv_addr = ctypes.addressof(packed_data)
        print("Python: vpfunc(%d, <%016x>, %d)" % (vptype, pv_addr, nele))
        r = self.clib.vpfunc(vptype, pv_addr, nele)
        print(r)


vp = VP()
vp.call_vpfunc([1, 2, 3, 4])
vp.call_vpfunc([1.1, 2.2, 3, 44.4, 5.5])
vp.call_vpfunc(['a', 'bb', 'ccc', '가나다', '우리는', '국민'])
