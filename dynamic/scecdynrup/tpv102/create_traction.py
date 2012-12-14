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

dTshear = 25.0e+6
T = 1.0
R = 3.0e+3
hypoX = 0.0
hypoY = 0.0
hypoZ = -7.5e+3
t = numpy.arange(0.0, 1.01001, 0.01)
t[-1] = 15.0

faultW = 18.0e+3
faultL = 36.0e+3
dx = 100.0

# ----------------------------------------------------------------------
def fnF(r):
    mask = r < R
    F = mask*numpy.exp(r**2/(r**2-R**2))
    F[~mask] = 0.0
    F[F < 1.0e-20] = 0.0
    return F

def fnG(t):
    mask1 = numpy.bitwise_and(0 < t, t < T)
    mask2 = t >= T
    G = mask1*numpy.exp((t-T)**2/(t*(t-2*T))) + mask2*1.0
    return G

# ----------------------------------------------------------------------
x = numpy.array([0.0], dtype=numpy.float64)
y = numpy.hstack((numpy.array([-0.5*faultL], dtype=numpy.float64),
                  numpy.arange(hypoY-R, hypoY+R+0.5*dx, dx, dtype=numpy.float64),
                  numpy.array([+0.5*faultL], dtype=numpy.float64)))
z = numpy.hstack((numpy.array([-faultW], dtype=numpy.float64),
                  numpy.arange(hypoZ-R, hypoZ+R+0.5*dx, dx, dtype=numpy.float64),
                  numpy.array([0.0], dtype=numpy.float64)))

nx = x.shape[0]
ny = y.shape[0]
nz = z.shape[0]
npts = nx*ny*nz
xyz = numpy.zeros( (npts, 3), dtype=numpy.float64)
xyz[:,0] = x
for iy in xrange(ny):
    xyz[iy*nz:(iy+1)*nz,1] = y[iy]
    xyz[iy*nz:(iy+1)*nz,2] = z

zero = numpy.zeros( (npts,), dtype=numpy.float64)

r = ((xyz[:,0]-hypoX)**2 + (xyz[:,1]-hypoY)**2 + (xyz[:,2]-hypoZ)**2)**0.5
tractionLL = dTshear*fnF(r)

cs = CSCart()
cs.initialize()

writer = SimpleGridAscii()
writer.inventory.filename = "traction_change.spatialdb"
writer._configure()
writer.write({'points': xyz,
              'x': x,
              'y': y,
              'z': z,
              'coordsys': cs,
              'data_dim': 2,
              'values': [{'name': "traction-shear-leftlateral",
                          'units': "MPa",
                          'data': tractionLL},
                         {'name': "traction-shear-updip",
                          'units': "MPa",
                          'data': zero},
                         {'name': "traction-normal",
                          'units': "MPa",
                          'data': zero},
                         {'name': "change-start-time",
                          'units': "s",
                          'data': zero},
                         ]})

# Time history
th = open("traction_change.timedb", "w")
th.write("#TIME HISTORY ascii\n" +
         "TimeHistory {\n" +
         "  num-points = %d\n" % t.shape[0] +
         "  time-units = s\n" +
         "}\n")
data = numpy.transpose((t, fnG(t)))
numpy.savetxt(th, data, fmt='%14.6e')
th.close()


# End of file

