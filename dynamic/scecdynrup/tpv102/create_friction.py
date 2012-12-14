#!/usr/bin/env python
# ----------------------------------------------------------------------
#
# Python script to create spatial database with rate-state friction parameters.
#
# Brad T. Aagaard, U.S. Geological Survey
#
# ----------------------------------------------------------------------
#
# PREREQUISITES: numpy, spatialdata

# ======================================================================
import numpy

from spatialdata.spatialdb.SimpleGridAscii import SimpleGridAscii
from spatialdata.geocoords.CSCart import CSCart

faultW = 18.0e+3
faultL = 36.0e+3
taperW = 3.0e+3
dx = 100.0
W = faultW - taperW

# ----------------------------------------------------------------------
def fnB(x, W, w):
    xabs = numpy.abs(x)
    mask1 = xabs <= W
    mask2 = numpy.bitwise_and(W < xabs, xabs < W+w)
    mask3 = xabs >= W+w
    v = 1.0*mask1 + 0.5*(1.0+numpy.tanh(w/(xabs-W-w) + w/(xabs-W)))*mask2 + 0.0*mask3
    return v

# ----------------------------------------------------------------------
x = numpy.array([0.0], dtype=numpy.float64)
y = numpy.arange(-0.5*faultL, 0.5*faultL+0.5*dx, dx, dtype=numpy.float64)
z = numpy.arange(-faultW, 0.0+0.5*dx, dx, dtype=numpy.float64)

nx = x.shape[0]
ny = y.shape[0]
nz = z.shape[0]
npts = nx*ny*nz
xyz = numpy.zeros( (npts, 3), dtype=numpy.float64)
xyz[:,0] = x
for iy in xrange(ny):
    xyz[iy*nz:(iy+1)*nz,1] = y[iy]
    xyz[iy*nz:(iy+1)*nz,2] = z

f0 = 0.6*numpy.ones( (npts,), dtype=numpy.float64)
v0 = 1.0e-6*numpy.ones( (npts,), dtype=numpy.float64)
a = 0.008 + 0.008*(1.0 - fnB(xyz[:,1], W, taperW)*fnB(-xyz[:,2]-7.5e+3,0.5*W,taperW))
b = 0.012*numpy.ones( (npts,), dtype=numpy.float64)
L = 0.02*numpy.ones( (npts,), dtype=numpy.float64)
cohesion = numpy.zeros( (npts,), dtype=numpy.float64)
vi = 1.0e-12
Tshear = 75.0e+6
Tnormal = -120.0e+6

theta0 = L/v0*numpy.exp(1.0/b*(-Tshear/Tnormal - f0 - a*numpy.log(vi/v0)))

cs = CSCart()
cs.initialize()

writer = SimpleGridAscii()
writer.inventory.filename = "friction.spatialdb"
writer._configure()
writer.write({'points': xyz,
              'x': x,
              'y': y,
              'z': z,
              'coordsys': cs,
              'data_dim': 2,
              'values': [{'name': "reference-friction-coefficient",
                          'units': "none",
                          'data': f0},
                         {'name': "reference-slip-rate",
                          'units': "m/s",
                          'data': v0},
                         {'name': "characteristic-slip-distance",
                          'units': "m",
                          'data': L},
                         {'name': "constitutive-parameter-a",
                          'units': "none",
                          'data': a},
                         {'name': "constitutive-parameter-b",
                          'units': "none",
                          'data': b},
                         {'name': "cohesion",
                          'units': "MPa",
                          'data': cohesion},
                         {'name': "state-variable",
                          'units': "s",
                          'data': theta0},
                         ]})


# End of file

