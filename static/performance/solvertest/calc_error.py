#!/usr/bin/env python

# Calculate error in solution field and fault tractions.

test = "revised_tol8"
base = "revised_smalltol"

import tables
import numpy

h5 = tables.openFile("output/%s.h5" % base, "r")
solnBase = h5.root.vertex_fields.displacement[:]
h5.close()

h5 = tables.openFile("output/%s.h5" % test, "a")
solnTest = h5.root.vertex_fields.displacement[:]

solnDiff = solnBase - solnTest
if "/vertex_fields/displacement_error" in h5:
    h5.removeNode("/vertex_fields/displacement_error")
h5.createArray("/vertex_fields", "displacement_error", solnDiff)
h5.copyNodeAttrs("/vertex_fields/displacement", 
                 "/vertex_fields/displacement_error")
h5.close()
