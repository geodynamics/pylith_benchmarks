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

shape = "tet4"
res = 500

# ----------------------------------------------------------------------
def getMap(solnfile):
    """
    Get element interpolation mapping information.
    """
    vertices = solnfile.root.geometry.vertices[:]
    (nvertices, spaceDim) = vertices.shape
    cells = solnfile.root.topology.cells[:]
    (ncells, ncorners) = cells.shape

    if spaceDim == 3 and ncorners == 4:
        from benchmark.discretize.Tet4 import Tet4
        cell = Tet4()
    else:
        raise ValueError("Unknown finite-element in dimension %d with %d " \
                         "corners." % (spaceDim, ncorners))
    return cell.calcMap(vertices, cells)


# ----------------------------------------------------------------------
def main_load_disp(app):
    """
    Local replacement for CompareApp::main().

    Load displacement fields.
    """
    
    field = "displacements"
    filename = "results/strikeslip_%s_%04dm.h5" % (shape, res)
    
    projection = app.projection
    projection.open()

    # PyLith ---------------------------------
    app._info.log("Projecting PyLith solution...")
    solnfile = tables.openFile(filename, 'r')
    solnmap = getMap(solnfile)
    for tstep in [0]:
        projection.project(solnfile, solnmap, "pylith_1_0", tstep, field)
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
    app.mainfn = main_load_disp
    app.run()
    app.mainfn = main_cmp_disp
    app.run()


# End of file
