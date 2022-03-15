import math

isometric = lambda x, y, z, offset_x=0, offset_y=0: (offset_x + x * 10 - y * 10, offset_y + x * 5 + y * 5 - z * 14)

def rev_isometric(isometricx, isometricy, z, offset_x=0, offset_y=0):
    y = ((isometricy - offset_y) / 5 - (isometricx - offset_x) / 10 + z * 14 / 5) / 2
    return ((isometricx - offset_x) / 10 + y, y)
