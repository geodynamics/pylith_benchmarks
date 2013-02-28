#!/usr/bin/env python
#
# ----------------------------------------------------------------------
#
#                           Brad T. Aagaard
#                        U.S. Geological Survey
#
# ----------------------------------------------------------------------
#

# Create spatial variation of friction parameters for TPV24-25 on the
# faults.

hypoy = -6.0e+3
hypoz = -10.0e+3
vs = 3464.0

# ----------------------------------------------------------------------
import numpy
from spatialdata.spatialdb.SimpleIOAscii import SimpleIOAscii
from spatialdata.geocoords.CSCart import CSCart

# ----------------------------------------------------------------------
# main fault
y = 1.0e+3*numpy.arange(-14.0, +14.001, 0.1)
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

coefStatic = 0.18*numpy.ones( (nptsy*nptsz), dtype=numpy.float64)
coefDyn = 0.12*numpy.ones( (nptsy*nptsz), dtype=numpy.float64)
d0 = 0.30*numpy.ones( (nptsy*nptsz), dtype=numpy.float64)
t0 = 0.50*numpy.ones( (nptsy*nptsz), dtype=numpy.float64)

mask = points[:,2] > -4000.0
cohesion = mask*(0.30+0.000675*(+4.0e+3+points[:,2])) + ~mask*0.30

rcrit = 4000.0
mask = r <= rcrit
weakTime = mask*(r/(0.7*vs) + 0.081*rcrit/(0.7*vs)*(1.0/(1.0-(r/rcrit)**2)-1)) + ~mask*1.0e+9

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
                       'units': 'MPa',
                       'data': cohesion},
                      {'name': 'time-weakening-time', 
                       'units': 's',
                       'data': weakTime},
                      {'name': 'time-weakening-parameter', 
                       'units': 's',
                       'data': t0},
                      ],
           }
writer.write(dataOut)


# ----------------------------------------------------------------------
# branch fault
x = 1.0e+3*numpy.arange(0.0, +6.001, 0.05)
z = 1.0e+3*numpy.arange(0.0, -15.001, -0.1)

nptsx = x.shape[0]
nptsz = z.shape[0]

points = numpy.zeros( (nptsx*nptsz, 3), dtype=numpy.float64)
for i in xrange(nptsz):
    istart = i
    istop = i+nptsx*nptsz
    points[istart:istop:nptsz,1] = x
for i in xrange(nptsx):
    istart = i*nptsz
    istop = (i+1)*nptsz
    points[istart:istop,2] = z

coefStatic = 0.18*numpy.ones( (nptsx*nptsz), dtype=numpy.float64)
coefDyn = 0.12*numpy.ones( (nptsx*nptsz), dtype=numpy.float64)
d0 = 0.30*numpy.ones( (nptsx*nptsz), dtype=numpy.float64)

mask = points[:,2] > -4000.0
cohesion = mask*(0.30+0.000675*(+4.0e+3+points[:,2])) + ~mask*0.30

writer = SimpleIOAscii()
writer.inventory.filename = "empty"
writer._configure()

writer.filename("friction_branch.spatialdb")
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
                       'units': 'MPa',
                       'data': cohesion},
                      ],
           }
writer.write(dataOut)


# End of file
