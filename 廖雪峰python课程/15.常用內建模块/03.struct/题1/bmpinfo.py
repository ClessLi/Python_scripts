import sys
import struct

def checkbmp(file):
    f_info=struct.unpack('<ccIIIIIIHH',file)
    if f_info[0:2]==('B','M'):
        print '''%s:
        Size: %s x %s.
        color: %s''' % (sys.argv[1],[6],f_info[7],f_info[9])
    else:
        print '%s is not a bmp file.' % sys.argv[1]

try:
    f=open(sys.argv[1],'r')
    checkbmp(f)
finally:
    if f:
        f.close()