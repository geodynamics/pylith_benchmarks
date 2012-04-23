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

analyticalFile = "../analytical/savpres_displ.csv"
numericalFiles = ["../output/sp_hex8/sp_hex8-groundsurf.h5",
                  "../output/sp_tet4/sp_tet4-groundsurf.h5"]
# The indices for analytical solution need changing for time step size of 10.
anlRefCol = 370
anlOutputCols = [372, 380, 390, 400, 408]
# End change.
numRefStep = 180
numOutputSteps = [181, 185, 190, 195, 199]
numSteps = 5
numPlots = 2
anlHeaderLines = 5

style = "lightbg"
plotSize = "poster"
outputFiles = ["spbm_hex8.eps", "spbm_tet4.eps"]
coseismicDispl = 4.0
elasticThick = 4.0e4

# ======================================================================
import numpy
import pylab
import tables
from Figure import Figure

# ----------------------------------------------------------------------
class ProfileSet(object):
  """
  Get profiles for analytical solution.
  """

  def __init__(self, filename, solnType):
    if (solnType == "analytical"):
      # Analytical solution stuff is completely broken for the new analytical
      # output.  I was just starting to fix it.
      f = open(filename, 'r')
      for line in range(anlHeaderLines):
        
      soln = numpy.loadtxt(filename, comments="#", dtype=numpy.float64)
      self.xCoord = soln[:,0]/elasticThick
      numPoints = self.xCoord.shape[0]
      refDispl = soln[:,anlRefCol]
      self.data = (soln[:,anlOutputCols] - refDispl)/coseismicDispl
    else:
      # Open file and get coordinates
      h5 = tables.openFile(filename, "r")
      coords = h5.root.geometry.vertices[:]

      # Get coordinate indices for y == 0.0 and x >= 0.0
      yProf = coords[:,1] == 0.0
      posVals = coords[:,0] >= 0.0
      posProf = numpy.logical_and(yProf, posVals)
      posProfInds = numpy.nonzero(posProf)

      # Get solution, and then remove profile indices that give negative displ.
      soln = h5.root.vertex_fields.displacement[:]
      solnTest = soln[numRefStep, posProfInds, 1]
      negInd = numpy.nonzero(solnTest < 0.0)[1][0]
      profileInds = numpy.delete(posProfInds, negInd)

      # Get test profile coordinates and then sort key.
      profCoords = coords[profileInds, 0]
      coordSort = numpy.argsort(profCoords)
      profInds = profileInds[coordSort]

      # Get coordinates and solution.
      self.xCoord = coords[profInds, 0]/elasticThick
      numPoints = self.xCoord.shape[0]
      refDispl = soln[numRefStep, profInds, 1]
      refDisplReshape = numpy.column_stack((refDispl, refDispl, refDispl,
                                            refDispl, refDispl))
      solnSteps = soln[numOutputSteps, :, 1]
      self.data = (solnSteps[:, profInds].transpose() - refDisplReshape)/coseismicDispl
      
    return


  def plot(self, linestyle, linewidth):
    data = self.data
    xCoord = self.xCoord

    colorOrder = ('orange', 'blue', 'red', 'green', 'purple')
    for step in range(numSteps):
      h = pylab.plot(xCoord, data[:,step], linestyle, linewidth=linewidth,
                     color=colorOrder[step])
    return h


# ----------------------------------------------------------------------
class Profiles(Figure):
  """
  Figure with displacement time histories for a site.
  """

  def __init__(self, plotNum):
    if plotSize == "poster":
      fontsize = 14
    elif plotSize == "presentation":
      fontsize = 14
    elif plotSize == "manual":
      fontsize = 10
    else:
      raise ValueError("Unknown plotSize '%s'." % plotSize)
    Figure.__init__(self, color=style, fontsize=fontsize)
    self.plotNum = plotNum
    
    return


  def plot(self):

    self.width = 7.25
    self.height = 5.0

    # Create figure
    self.open(self.width, self.height, margins=[[0.70, 0, 0.20],
                                                [0.55, 0, 0.12]])

    # Plot profiles
    self.axes(1, 1, 1, 1)
    analytic = ProfileSet(analyticalFile, "analytical")
    ah = analytic.plot(linestyle="-", linewidth=1)
    pylab.hold(True)
    simulationFile = numericalFiles[self.plotNum]
    simulation = ProfileSet(simulationFile, "numerical")
    sh = simulation.plot(linestyle="--", linewidth=1)
    pylab.hold(False)

    pylab.xlim(0, 10)
    pylab.ylim(0, 0.5)

    leg = pylab.legend((ah, sh),
                       ["analytic", "simulation"],
                       loc="upper left")
    leg.legendPatch.set_facecolor('bg')
    leg.legendPatch.set_edgecolor('fg')
    self._annotate()
    return


  def save(self):
    pylab.figure(self.handle.number)
    outputFile = outputFiles[self.plotNum]
    pylab.savefig(outputFile)
    return


  def _annotate(self):
    """
    Add title and labels for axes.
    """
    pylab.xlabel("Dist. from fault / Elastic thickness")
    pylab.ylabel("Disp. / Coseismic Disp. ")

    pylab.text(9.9, 0.03, "t=0.05", horizontalalignment="right")
    pylab.text(9.9, 0.13, "t=0.25", horizontalalignment="right")
    pylab.text(9.9, 0.255, "t=0.50", horizontalalignment="right")
    pylab.text(9.9, 0.37, "t=0.75", horizontalalignment="right")
    pylab.text(9.9, 0.46, "t=0.95", horizontalalignment="right")
    return


# ----------------------------------------------------------------------
if __name__ == "__main__":

  import pdb
  pdb.set_trace()

  figures = []
  for plotNum in range(numPlots):
    figure = Profiles(plotNum)
    figure.plot()
    figures.append(figure)

  pylab.show()
  for figure in figures:
    figure.save()

# End of file
