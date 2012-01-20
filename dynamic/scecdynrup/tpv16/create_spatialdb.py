#!/usr/bin/env python
#
# ----------------------------------------------------------------------
#
#                           Brad T. Aagaard
#                        U.S. Geological Survey
#
# ----------------------------------------------------------------------
#

# Requires input files from SCEC website.
# http://scecdata.usc.edu/cvws/download/tpv16/tpv16_17_input_files.zip

sim = "tpv17"

# ----------------------------------------------------------------------
import numpy
from spatialdata.spatialdb.SimpleIOAscii import SimpleIOAscii
from spatialdata.geocoords.CSCart import CSCart

data = numpy.loadtxt("%s_input_file.txt" % sim, skiprows=3)

points = numpy.transpose((0*data[:,2], data[:,2]-24.0e+3, -data[:,3]))

tractionNormal = -data[:,4]
tractionShearHoriz = -data[:,5]
tractionShearVert = data[:,6]

coefStatic = data[:,9]
coefDyn = data[:,10]
d0 = data[:,11]
cohesion = data[:,12]
weakTime = data[:,13]


cs = CSCart()
cs._configure()
cs.initialize()

writer = SimpleIOAscii()
writer.inventory.filename = "empty"
writer._configure()

writer.filename("%s_tractions.spatialdb" % sim)
dataOut = {'points': points,
           'coordsys': cs,
           'data_dim': 2,
           'values': [{'name': 'traction-shear-leftlateral', 
                       'units': 'Pa',
                       'data': tractionShearHoriz},
                      {'name': 'traction-shear-updip',
                       'units': 'Pa',
                       'data': tractionShearVert},
                      {'name': 'traction-normal',
                       'units': 'Pa',
                       'data': tractionNormal},
                      ],
           }

writer.write(dataOut)

writer.filename("%s_friction.spatialdb" % sim)
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
