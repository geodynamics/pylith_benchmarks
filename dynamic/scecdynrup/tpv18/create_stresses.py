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
# TPV18-21. Initial stresses are only used in TPV19 and TPV21.

sim = "tpv18"

# ----------------------------------------------------------------------
# Parameters from benchmark description
gacc = 9.8
density = 2700
densityW = 1000.0

if sim == "tpv18" or sim == "tpv19":
    b22 = 0.44327040
    b33 = 0.50911055
    b23 = -0.15487679
elif sim == "tpv20" or sim == "tpv21":
    b22 = 0.67738619
    b33 = 0.27499476
    b23 = 0.09812971
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

Syy = mask1*(b22*(Szz+Pf)-Pf) + ~mask1*Szz
Sxx = mask1*(b33*(Szz+Pf)-Pf) + ~mask1*Szz
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
writer.write(dataOut)


# ----------------------------------------------------------------------
# Initial tractions on main fault

# Fault normal
nx = 1.0
ny = 0.0
nz = 0.0

# normal traction is Tx
tractionNormal = Sxx*nx + Sxy*ny + Sxz*nz

# LL shear traction is Ty
tractionShearLL = Sxy*nx + Syy*ny + Syz*nz

# Up-dip shear traction is Tz
tractionShearUD = Sxz*nx + Syz*ny + Szz*nz

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

# normal traction is Tx
tractionNormal = Sxx*nx + Sxy*ny + Sxz*nz

# LL shear traction is Ty
tractionShearLL = Sxy*nx + Syy*ny + Syz*nz

# Up-dip shear traction is Tz
tractionShearUD = Sxz*nx + Syz*ny + Szz*nz

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
