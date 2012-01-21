#!/usr/bin/env python
#
# ----------------------------------------------------------------------
#
#                           Brad T. Aagaard
#                        U.S. Geological Survey
#
# ----------------------------------------------------------------------
#

# Create spatial variation of friction parameters for TPV18-21 on main
# fault.

hypoy = 2.0e+3-8.0e+3
hypoz = -7.5e+3
vs = 3300.0

# ----------------------------------------------------------------------
import numpy
from spatialdata.spatialdb.SimpleIOAscii import SimpleIOAscii
from spatialdata.geocoords.CSCart import CSCart

y = 1.0e+3*numpy.arange(-15.0, +15.001, 0.1)
z = 1.0e+3*numpy.arange(0.0, -15.001, -0.1)

nptsy = y.shape[0]
nptsz = z.shape[0]

points = numpy.zeros( (nptsy*nptsz, 3), dtype=numpy.float64)
for i in xrange(nptsz):
    istart = i
    istop = i+nptsy*nptsz
    points[istart:istop:nptsz,1] = y
for i in xrange(nptsy):
    istart = i*nptsz
    istop = (i+1)*nptsz
    points[istart:istop,2] = z

r = ( (points[:,1]-hypoy)**2 +
      (points[:,2]-hypoz)**2)**0.5

coefStatic = 0.6*numpy.ones( (nptsy*nptsz), dtype=numpy.float64)
coefDyn = 0.12*numpy.ones( (nptsy*nptsz), dtype=numpy.float64)

mask1 = r <= 360.0
mask2 = numpy.bitwise_and(r > 360.0, r <= 3600.0)
mask3 = r > 3600.0
d0 = mask1*0.04 + mask2*r/9000.0 + mask3*0.40


mask1 = points[:,2] > -3000.0
mask2 = points[:,2] <= -3000.0
cohesion = mask1*(0.20 + 0.0006*(points[:,2]+3000.0)) + mask2*0.20

mask1 = r <= 720.0
mask2 = numpy.bitwise_and(r > 720.0, r <= 900.0)
mask3 = r > 900.0
weakTime = mask1*r/(0.7*vs) + mask2*(720.0/(0.7*vs) + (r-720)/(0.35*vs)) + mask3*1.0e+9

mask1 = points[:,1] <= -14.999e+3
coefStatic[mask1] = 1.0e+6
mask1 = points[:,1] >= +14.999e+3
coefStatic[mask1] = 1.0e+6
mask1 = points[:,2] <= -14.999e+3
coefStatic[mask1] = 1.0e+6


cs = CSCart()
cs._configure()
cs.initialize()

writer = SimpleIOAscii()
writer.inventory.filename = "empty"
writer._configure()

writer.filename("friction_main.spatialdb")
dataOut = {'points': points,
           'coordsys': cs,
           'data_dim': 2,
           'values': [{'name': 'static-coefficient', 
                       'units': 'None',
                       'data': coefStatic},
                      {'name': 'dynamic-coefficient', 
                       'units': 'None',
                       'data': coefDyn},
                      {'name': 'slip-weakening-parameter', 
                       'units': 'm',
                       'data': d0},
                      {'name': 'cohesion', 
                       'units': 'Pa',
                       'data': cohesion},
                      {'name': 'weakening-time', 
                       'units': 's',
                       'data': weakTime},
                      ],
           }
writer.write(dataOut)


# End of file
