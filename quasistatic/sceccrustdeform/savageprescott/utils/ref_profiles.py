#!/usr/bin/env python
#
# ----------------------------------------------------------------------
#
#                           Brad T. Aagaard
#                        U.S. Geological Survey
#
# <LicenseText>
#
# ----------------------------------------------------------------------
#

## @file utils/ref_profiles

## @brief Python application to reference displacement profiles to a profile
## at the beginning of a cycle.

import math
import numpy
import pylab
from pyre.units.time import s

from pyre.applications.Script import Script as Application

class RefProfiles(Application):
  """
  Python application to reference displacement profiles to a profile at the
  beginning of an earthquake cycle.
  """
  
  class Inventory(Application.Inventory):
    """
    Python object for managing RefProfiles facilities and properties.
    """

    ## @class Inventory
    ## Python object for managing VtkDiff facilities and properties.
    ##
    ## \b Properties
    ## @li \b input_file Input file, consisting of tab-delimited values.
    ## @li \b output_root Root name for output file(s).
    ## @li \b displ_scale_factor Scale factor to apply to displacements.
    ## @li \b coord_scale_factor Scale factor to apply to coordinates.
    ## @li \b num_cycles Number of earthquake cycles.
    ## @li \b steps_per_cycle Number of steps per earthquake cycle.
    ## @li \b delimiter Column delimiter (use only if other than whitespace).

    import pyre.inventory

    inputFile = pyre.inventory.str("input_file", default="input.txt")
    inputFile.meta['tip'] = "Input filename (tab-delimited text)."

    outputRoot = pyre.inventory.str("output_root", default="output.txt")
    outputRoot.meta['tip'] = "Root output filename."

    displScaleFactor = pyre.inventory.float("displ_scale_factor", default=1.0)
    displScaleFactor.meta['tip'] = "Scaling factor to apply to displacements."

    coordScaleFactor = pyre.inventory.float("coord_scale_factor", default=1.0)
    coordScaleFactor.meta['tip'] = "Scaling factor to apply to coordinates."

    numCycles = pyre.inventory.int("num_cycles", default=10)
    numCycles.meta['tip'] = "Number of earthquake cycles."

    stepsPerCycle = pyre.inventory.int("steps_per_cycle", default=20)
    stepsPerCycle.meta['tip'] = "Number of time steps per earthquake cycle."

    delimiter = pyre.inventory.str("delimiter", default=None)
    delimiter.meta['tip'] = "Column delimiter (use only if other than whitespace)."


  # PUBLIC METHODS /////////////////////////////////////////////////////

  def __init__(self, name="ref_profiles"):
    Application.__init__(self, name)
    return


  def main(self):
    # import pdb
    # pdb.set_trace()
    if self.delimiter != None:
      self.data = numpy.loadtxt(self.inputFile, delimiter=self.delimiter)
    else:
      self.data = numpy.loadtxt(self.inputFile)
    self._refProfiles()
    return


  # PRIVATE METHODS ////////////////////////////////////////////////////

  def _configure(self):
    """
    Setup members using inventory.
    """
    Application._configure(self)
    import os

    # Set up info describing data
    self.displScaleFactor = self.inventory.displScaleFactor
    self.coordScaleFactor = self.inventory.coordScaleFactor
    self.numCycles = self.inventory.numCycles
    self.stepsPerCycle = self.inventory.stepsPerCycle
    self.delimiter = self.inventory.delimiter

    # Set up i/o info
    self.inputFile = self.inventory.inputFile
    totalOutputPath = os.path.normpath(os.path.join(
      os.getcwd(), self.inventory.outputRoot))
    self.outputDir = os.path.dirname(totalOutputPath)
    baseOutputName = os.path.basename(totalOutputPath)
    baseOutputNameLen = len(baseOutputName)
    if baseOutputName.endswith(".txt"):
      baseOutputNameStripped = baseOutputName[0:baseOutputNameLen - 4]
    else:
      baseOutputNameStripped = baseOutputName
    self.outputRoot = baseOutputNameStripped
    if not os.path.isdir(self.outputDir):
      os.mkdir(self.outputDir)

    return


  def _refProfiles(self):
    """
    Reference profiles to the first step in a cycle.
    """
    import os
    
    col0 = self.coordScaleFactor * self.data[:,0]
    numRows = col0.shape[0]
    col0Shaped = numpy.reshape(col0, (numRows, 1))
    for cycle in range(self.numCycles):
      startCycle = cycle * self.stepsPerCycle + 1
      cycleData = self.data[:,startCycle:startCycle + self.stepsPerCycle]
      cycleRef = numpy.copy(cycleData[:,0])
      for step in range(self.stepsPerCycle):
        cycleData[:,step] -= cycleRef
      cycleData *= self.displScaleFactor
      dataOut = numpy.concatenate((col0Shaped, cycleData), axis = 1)
      outputFileName = self.outputRoot + repr(cycle) + ".txt"
      outputFile = os.path.join(self.outputDir, outputFileName)
      numpy.savetxt(outputFile, dataOut)

    return
# ----------------------------------------------------------------------
if __name__ == '__main__':
  app = RefProfiles()
  app.run()

# End of file
