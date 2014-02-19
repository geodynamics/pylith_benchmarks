#!/usr/bin/env python

# Python script to create Exodus II mapped mesh of fault geometry for
# import into CUBIT.

# Filename for ExodusII file (output)
filenameEXO = "fault.exo"

# Geometry of simulation domain
domainLength = 64.0e+3
domainHeight = 32.0e+3
buffer = 2.0e+3 # Extend fault plane beyond domain

# Geometry of bump
bumpRadius = 3.0e+3
bumpAmplitude = 6.0e+2
bumpY = 10.5e+3
bumpZ = -7.5e+3
bumpDx = 5.0e+2

# ======================================================================
import os
import numpy

from cubit_io import write_exodus_file
from netCDF4 import Dataset

# ----------------------------------------------------------------------
def bump(yz):
    y = yz[:,0]
    z = yz[:,1]
    r1 = ((y+bumpY)**2 + (z-bumpZ)**2)**0.5
    r2 = ((y-bumpY)**2 + (z-bumpZ)**2)**0.5
    mask1 = r1 <= 3.0e+3
    mask2 = r2 <= 3.0e+3
    npts = yz.shape[0]
    x = mask1*+0.5*bumpAmplitude*(1.0+numpy.cos(numpy.pi*r1/3.0e+3)) + \
        mask2*+0.5*bumpAmplitude*(1.0+numpy.cos(numpy.pi*r2/3.0e+3))
    return x


# ----------------------------------------------------------------------
yA = numpy.linspace(-0.5*domainLength-buffer, -bumpY-bumpRadius, 2)
yB = numpy.arange(-bumpY-bumpRadius+bumpDx, -bumpY+bumpRadius, bumpDx)
yC = numpy.linspace(-bumpY+bumpRadius, +bumpY-bumpRadius, 2)
yD = numpy.arange(+bumpY-bumpRadius+bumpDx, +bumpY+bumpRadius, bumpDx)
yE = numpy.linspace(+bumpY+bumpRadius, +0.5*domainLength+buffer, 2)
y = numpy.hstack((yA, yB, yC, yD, yE))
numY = y.shape[0]

zA = numpy.linspace(-domainHeight-buffer, bumpZ-bumpRadius, 2)
zB = numpy.arange(bumpZ-bumpRadius+bumpDx, bumpZ+bumpRadius, bumpDx)
zC = numpy.linspace(bumpZ+bumpRadius, 0.0, 2)
z = numpy.hstack((zA, zB, zC))
numZ = z.shape[0]

yz = numpy.zeros((numY*numZ, 2), dtype=numpy.float64)

for iY in xrange(numY):
    yz[iY*numZ:(iY+1)*numZ,1] = z
    yz[iY*numZ:(iY+1)*numZ,0] = y[iY]

x = bump(yz)
vertices = numpy.zeros((numY*numZ,3), dtype=numpy.float64)
vertices[:,0] = x
vertices[:,1] = yz[:,0]
vertices[:,2] = yz[:,1]

cells = numpy.zeros(((numY-1)*(numZ-1),4), dtype=numpy.int32)

for iY in xrange(numY-1):
    for iZ in xrange(numZ-1):
        v0 = iY*numZ+iZ
        v1 = v0+1
        v2 = v1+numZ
        v3 = v0+numZ
        cells[iY*(numZ-1)+iZ,:] = [v0,v1,v2,v3]

write_exodus_file(filenameEXO, cells, vertices)


# End of file
