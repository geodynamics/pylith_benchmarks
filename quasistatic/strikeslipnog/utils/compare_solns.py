#!/usr/bin/env python
#
# ======================================================================
#
#                           Brad T. Aagaard
#                        U.S. Geological Survey
#
# {LicenseText}
#
# ======================================================================
#

## @brief Python script to compare benchmark solutions.

import tables

shape = "hex8"
res = 1000

# ----------------------------------------------------------------------
def main_load_disp(app):
    """
    Local replacement for CompareApp::main().

    Load displacement fields.
    """
    
    field = "displacements"
    filename = "results/strikeslip_%s_%04dm.h5" % (shape, res)
    
    projection.open()

    # PyLith ---------------------------------
    app._info.log("Projecting PyLith solution...")
    solnfile = tables.openFile(filename, 'r')
    for tstep in [0]:
        projection.project(solnfile, "pylith_1_0", tstep, field)
    solnfile.close()

    # Analytic -------------------------------
    app._info.log("Copying analytic solution...")
    filename = "analytic/output/%s_%04dm.h5" % (shape, res)
    solnfile = tables.openFile(filename, 'r')
    for tstep in [0]:
        projection.copy_projection(solnfile, "analytic", tstep, field)
    solnfile.close()

    # ----------------------------------------
    projection.close()

    return

# ----------------------------------------------------------------------
def main_cmp_disp(app):
    """
    Local replacement for CompareApp::main().

    Compare displacement fields.
    """
    
    field = "displacements"
    
    projection = app.projection
    
    projection.open()

    # Code versus analytic -------------------
    tstep = 0
    print "Time Step: %d" % tstep

    err = projection.difference(tstep, field, "pylith_1_0", "analytic")
    print "PyLith-1.0, error wrt analytic: %12.4e" % err
    
    # ----------------------------------------
    projection.close()

    return


# ----------------------------------------------------------------------
if __name__ == "__main__":

    from pkg_resources import require
    require("merlin>=1.0")
    require("pythia>=0.8")

    import journal
    journal.info("compareapp").activate()

    from benchmark.CompareApp import CompareApp
    app = CompareApp()
    app._configure()
    projection = app.projection
    if shape == "tet4":
        from benchmark.discretize.FIATSimplex import FIATSimplex
        projection.discretize = FIATSimplex()
    elif shape == "hex8":
        from benchmark.discretize.FIATLagrange import FIATLagrange
        projection.discretize = FIATLagrange()
    projection.discretize._configure()
    projection.discretize.initialize()
    
    app.mainfn = main_load_disp
    app.run()
    app.mainfn = main_cmp_disp
    app.run()


# End of file
