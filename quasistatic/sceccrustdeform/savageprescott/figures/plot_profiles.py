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

cycles = [2,9]
style = "lightbg"
fileSuffix = "eps"
plotSize = "poster"

# ======================================================================
import numpy
import pylab
from mypylab.Figure import Figure

# ----------------------------------------------------------------------
class ProfileSet(object):
  """
  Set of profiles.
  """

  def __init__(self, filename):
    self.data = numpy.loadtxt(filename, comments="#")
    ncols = self.data.shape[1]
    self.data[:,1:ncols+1] /= 400.0 # Coseismic displacement
    self.data[:,0] /= 40.0 # Thickness of elastic layer
    return


  def plot(self, linestyle):
    data = self.data
    ncols = data.shape[1]
    if ncols == 42:
      indicesTime = [2, 10, 20, 30, 38]
    elif ncols == 21:
      indicesTime = [1, 5, 10, 15, 19]

    colorOrder = ('orange', 'blue', 'red', 'green', 'purple')
    i = 0
    for index in indicesTime:
      h = pylab.plot(data[:,0], data[:,1+index], linestyle, color=colorOrder[i])
      i += 1
    return h


# ----------------------------------------------------------------------
class Profiles(Figure):
  """
  Figure with velocity time histories for a site.
  """

  def __init__(self, cycle):
    if plotSize == "poster":
      fontsize = 14
    elif plotSize == "presentation":
      fontsize = 14
    elif plotSize == "manual":
      fontsize = 10
    else:
      raise ValueError("Unknown plotSize '%s'." % plotSize)
    Figure.__init__(self, color=style, fontsize=fontsize)
    self.cycle = cycle
    return


  def plot(self):

    self.width = 7.25
    self.height = 5.0

    # Create figure
    self.open(self.width, self.height, margins=[[0.70, 0, 0.20],
                                                [0.55, 0, 0.12]])

    # Plot profiles
    self.axes(1, 1, 1, 1)
    analytic = ProfileSet("savpres_displ_c%dref.txt" % self.cycle)
    ah = analytic.plot(linestyle="-")
    pylab.hold(True)
    simulation = ProfileSet("spbm_hex8_graded_c%dref.txt" % self.cycle)
    sh = simulation.plot(linestyle="--")
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
    pylab.savefig("spbm_hex8_graded_profile%d.%s" % (self.cycle, fileSuffix))
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

  figures = []
  for cycle in cycles:
    figure = Profiles(cycle)
    figure.plot()
    figures.append(figure)

  pylab.show()
  for figure in figures:
    figure.save()

# End of file
