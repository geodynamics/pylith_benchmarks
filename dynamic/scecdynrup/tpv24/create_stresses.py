#!/usr/bin/env python
#
# ----------------------------------------------------------------------
#
#                           Brad T. Aagaard
#                        U.S. Geological Survey
#
# ----------------------------------------------------------------------
#

# Create spatial variation of initial stresses and fault tractions for
# TPV24-25.

sim = "tpv24"

# ----------------------------------------------------------------------
# Parameters from benchmark description
gacc = 9.8
density = 2670
densityW = 1000.0

if sim == "tpv24":
    b22 = 0.926793
    b33 = 1.073206
    b23 = -0.169029
elif sim == "tpv25":
    b22 = 1.119338
    b33 = 0.880661
    b23 = 0.138704
else:
    raise ValueError("Unknown simulation '%s'." % sim)


# ----------------------------------------------------------------------
import numpy
from spatialdata.spatialdb.SimpleIOAscii import SimpleIOAscii
from spatialdata.geocoords.CSCart import CSCart

z = numpy.array([0.0, -15.0e+3, -50e+3], dtype=numpy.float64)
points = numpy.zeros( (z.shape[0], 3), dtype=numpy.float64)
points[:,2] = z

cs = CSCart()
cs._configure()
cs.initialize()


mask1 = z >= -15.0e+3

Pf = -densityW*gacc*z
Szz = density*gacc*z

Syy = mask1*(b22*(Szz+Pf)-0*Pf) + ~mask1*Szz
Sxx = mask1*(b33*(Szz+Pf)-0*Pf) + ~mask1*Szz
Sxy = mask1*(-b23*(Szz+Pf)) + ~mask1*0.0

Syz = 0.0*z
Sxz = 0.0*z

writer = SimpleIOAscii()
writer.inventory.filename = "empty"
writer._configure()


# ----------------------------------------------------------------------
# Initial stresses in domain
writer.filename("%s_initial_stress.spatialdb" % sim)
dataOut = {'points': points,
           'coordsys': cs,
           'data_dim': 1,
           'values': [{'name': 'stress-xx', 
                       'units': 'Pa',
                       'data': Sxx},
                      {'name': 'stress-yy', 
                       'units': 'Pa',
                       'data': Syy},
                      {'name': 'stress-zz', 
                       'units': 'Pa',
                       'data': Szz},
                      {'name': 'stress-xy', 
                       'units': 'Pa',
                       'data': Sxy},
                      {'name': 'stress-yz', 
                       'units': 'Pa',
                       'data': Syz},
                      {'name': 'stress-xz', 
                       'units': 'Pa',
                       'data': Sxz},
                      ],
           }
#writer.write(dataOut) # Skip writing file that isn't used.


# ----------------------------------------------------------------------
# Initial tractions on main fault

# Fault normal
nx = 1.0
ny = 0.0
nz = 0.0

Tx = Sxx*nx + Sxy*ny + Sxz*nz
Ty = Sxy*nx + Syy*ny + Syz*nz
Tz = Sxz*nx + Syz*ny + Szz*nz

tractionNormal = Tx*nx + Ty*ny + Tz*nz
sx = 0.0
sy = 1.0
sz = 0.0
tractionShearLL = Tx*sx + Ty*sy + Tz*sz
sx = 0.0
sy = 0.0
sz = 1.0
tractionShearUD = Tx*sx + Ty*sy + Tz*sz

writer.filename("%s_traction_main.spatialdb" % sim)
dataOut = {'points': points,
           'coordsys': cs,
           'data_dim': 1,
           'values': [{'name': 'traction-shear-leftlateral', 
                       'units': 'Pa',
                       'data': tractionShearLL},
                      {'name': 'traction-shear-updip', 
                       'units': 'Pa',
                       'data': tractionShearUD},
                      {'name': 'traction-normal', 
                       'units': 'Pa',
                       'data': tractionNormal},
                      ],
           }
writer.write(dataOut)


# ----------------------------------------------------------------------
# Initial tractions on branch fault

# Fault normal
from math import sin,cos,pi
branchAngle = 30.0/180.0*pi
nx = cos(branchAngle)
ny = -sin(branchAngle)
nz = 0.0

Tx = Sxx*nx + Sxy*ny + Sxz*nz
Ty = Sxy*nx + Syy*ny + Syz*nz
Tz = Sxz*nx + Syz*ny + Szz*nz

tractionNormal = Tx*nx + Ty*ny + Tz*nz
sx = sin(branchAngle)
sy = cos(branchAngle)
sz = 0.0
tractionShearLL = Tx*sx + Ty*sy + Tz*sz
sx = 0.0
sy = 0.0
sz = 1.0
tractionShearUD = Tx*sx + Ty*sy + Tz*sz

writer.filename("%s_traction_branch.spatialdb" % sim)
dataOut = {'points': points,
           'coordsys': cs,
           'data_dim': 1,
           'values': [{'name': 'traction-shear-leftlateral', 
                       'units': 'Pa',
                       'data': tractionShearLL},
                      {'name': 'traction-shear-updip', 
                       'units': 'Pa',
                       'data': tractionShearUD},
                      {'name': 'traction-normal', 
                       'units': 'Pa',
                       'data': tractionNormal},
                      ],
           }
writer.write(dataOut)


# End of file
