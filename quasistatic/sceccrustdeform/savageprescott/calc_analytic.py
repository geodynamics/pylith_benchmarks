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

## @brief Python application to compute the Savage and Prescott [1978]
## solution for an infinitely long strike-slip fault embedded in an
## elastic layer overlying a viscoelastic half-space.

import math
import numpy

from pyre.applications.Script import Script as Application

class AnalyticalSoln(Application):
  """
  Python application to compute the Savage and Prescott [1978] solution
  for an infinitely long strike-slip fault embedded in an elastic layer
  overlying a viscoelastic half-space.
  """
  
  class Inventory(Application.Inventory):
    """
    Python object for managing facilities and properties.
    """

    ## @class Inventory
    ## Python object for managing Savpres_ss facilities and properties.
    ##
    ## \b Properties
    ## @li \b elas_thick Thickness of elastic layer.
    ## @li \b lock_depth Fault locking depth (<= elas_thick).
    ## @li \b recurrence_time Earthquake recurrence time.
    ## @li \b viscosity Viscosity of viscoelastic half-space.
    ## @li \b shear_modulus Shear modulus of layer and half-space.
    ## @li \b plate_velocity Relative plate velocity (left-lateral) across fault.
    ## @li \b number_cycles Number of earthquake cycles to compute.
    ## @li \b number_steps Number of time steps to compute for each cycle.
    ## @li \b number_terms Number of terms to compute for series solution.
    ## @li \b number_points Number of points at which to compute solution.
    ## @li \b delta_x Distance between computation points.
    ## @li \b x_epsilon Offset for computation point closest to the fault.
    ## @li \b output_disp Output displacement results?
    ## @li \b output_vel Output velocity results?
    ## @li \b disp_basename Base name for displacement output files.
    ## @li \b vel_basename Base name for velocity output files.

    import pyre.inventory
    from pyre.units.length import m,km,cm
    from pyre.units.time import s,year
    from pyre.units.pressure import Pa,MPa,GPa

    elasThick = pyre.inventory.dimensional("elas_thick", default=20.0*km)
    elasThick.meta['tip'] = "Thickness of elastic layer."

    lockDepth = pyre.inventory.dimensional("lock_depth", default=10.0*km)
    lockDepth.meta['tip'] = "Fault locking depth (<= elastic thickness)."

    recurrenceTime = pyre.inventory.dimensional("recurrence_time",
                                                default=100.0*year)
    recurrenceTime.meta['tip'] = "Earthquake recurrence time."

    viscosity = pyre.inventory.dimensional("viscosity", default=1.0e+18*Pa*s)
    viscosity.meta['tip'] = "Half-space viscosity."

    shearModulus = pyre.inventory.dimensional("shear_modulus", default=30.0*GPa)
    shearModulus.meta['tip'] = "Shear modulus of layer and half-space."

    plateVelocity = pyre.inventory.dimensional("plate_velocity",
                                               default=2.0*cm/year)
    plateVelocity.meta['tip'] = "Relative velocity (left-lateral) across the fault."

    numberCycles = pyre.inventory.int("number_cycles", default=10)
    numberCycles.meta['tip'] = "Number of earthquake cycles."

    numberSteps = pyre.inventory.int("number_steps", default=10)
    numberSteps.meta['tip'] = "Number of steps to compute for each cycle."

    numberTerms = pyre.inventory.int("number_terms", default=20)
    numberTerms.meta['tip'] = "Number of terms to compute for series."

    numberPoints = pyre.inventory.int("number_points", default=100)
    numberPoints.meta['tip'] = "Number of points at which to compute solution."

    deltaX = pyre.inventory.dimensional("delta_x", default=2.0*km)
    deltaX.meta['tip'] = "Distance between computation points."

    xEpsilon = pyre.inventory.dimensional("x_epsilon", default=0.001*m)
    xEpsilon.meta['tip'] = "Offset for computation point closest to the fault."

    outputDisp = pyre.inventory.bool("output_disp", default=True)
    outputDisp.meta['tip'] = "Output displacement files?"

    outputVel = pyre.inventory.bool("output_vel", default=True)
    outputVel.meta['tip'] = "Output velocity file?"

    dispfilename = pyre.inventory.str("disp_filename", 
                                      default="output/analytic_disp.txt")
    dispfilename.meta['tip'] = "Filename for displacement output."

    velfilename = pyre.inventory.str("vel_filename",
                                        default="output/analytic_vel.txt")
    velfilename.meta['tip'] = "Filename for velocity output."

  # PUBLIC METHODS /////////////////////////////////////////////////////

  def __init__(self, name="calc_analytic"):
    Application.__init__(self, name)
    return


  def main(self):
    self._genPoints()
    self._genSolution()
    if self.outputDisp:
      self._writeSolution("displacement")
    if self.outputVel:
      self._writeSolution("velocity")
    return


  # PRIVATE METHODS ////////////////////////////////////////////////////

  def _configure(self):
    """
    Setup members using inventory.
    """
    Application._configure(self)
    self.elasThick = self.inventory.elasThick
    self.lockDepth = self.inventory.lockDepth
    self.recurrenceTime = self.inventory.recurrenceTime
    self.viscosity = self.inventory.viscosity
    self.shearModulus = self.inventory.shearModulus
    self.velocity = self.inventory.plateVelocity / 2.0
    self.numberCycles = self.inventory.numberCycles
    self.numberSteps = self.inventory.numberSteps
    self.numberTerms = self.inventory.numberTerms
    self.numberPoints = self.inventory.numberPoints
    self.deltaX = self.inventory.deltaX
    self.xEpsilon = self.inventory.xEpsilon

    self.outputDisp = self.inventory.outputDisp
    self.outputVel = self.inventory.outputVel
    self.dispfilename = self.inventory.dispfilename
    self.velfilename = self.inventory.velfilename

    self.deltaT = self.recurrenceTime/self.numberSteps
    self.tauFac = 0.5*self.shearModulus/self.viscosity
    self.tau0 = self.recurrenceTime * self.tauFac

    return


  def _genPoints(self):
    """
    Create array of points for output along with series terms
    for each point.
    """
    self.points = numpy.zeros(self.numberPoints, dtype=numpy.float64)
    self.pointCoeff = numpy.zeros((self.numberPoints, self.numberTerms),
                                  dtype=numpy.float64)

    elasThick = self.elasThick.value
    lockDepth = self.lockDepth.value

    for point in range(self.numberPoints):
      self.points[point] = max(self.xEpsilon.value, point*self.deltaX.value)

      for term in range(self.numberTerms):
        n = term + 1
        coef = 2.0 * lockDepth * self.points[point] / \
            (4.0 * n**2 * elasThick**2 - lockDepth**2 + self.points[point]**2)
        self.pointCoeff[point, term] = coef

    self.pointCoeff = numpy.arctan(self.pointCoeff)

    return

    
  def _genSolution(self):
    """
    Compute transient solution.
    """
    solutionU2 = numpy.zeros((self.numberCycles,
                              self.numberSteps + 1,
                              self.numberPoints),
                             dtype=numpy.float64)
    self.solutionUTot = numpy.zeros((self.numberCycles,
                                     self.numberSteps + 1,
                                     self.numberPoints),
                                    dtype=numpy.float64)
    solutionV2 = numpy.zeros((self.numberCycles,
                              self.numberSteps + 1,
                              self.numberPoints),
                             dtype=numpy.float64)
    self.solutionVTot = numpy.zeros((self.numberCycles,
                                     self.numberSteps + 1,
                                     self.numberPoints),
                                    dtype=numpy.float64)
    oneArray = numpy.ones(self.numberPoints, dtype=numpy.float64)

    deltaT = self.deltaT.value
    tauFac = self.tauFac.value
    velocity = self.velocity.value


    for cycle in range(self.numberCycles):
      time = cycle * self.numberSteps * deltaT
      tau = time * tauFac
      if cycle > 0:
        solutionU2[cycle, :, :] += solutionU2[cycle - 1, :, :]
        solutionV2[cycle, :, :] += solutionV2[cycle - 1, :, :]

      for step in range(self.numberSteps + 1):
        if cycle == 0:
          solutionUT, solutionVT = self._u2A(tau)
        else:
          solutionUT, solutionVT = self._u2B(tau)

        solutionU2[cycle, step, :] += solutionUT
        solutionV2[cycle, step, :] += solutionVT
        self.solutionUTot[cycle, step, :] = solutionU2[cycle, step, :] + \
                                            time * velocity * oneArray
        self.solutionVTot[cycle, step, :] = tauFac * \
                                            solutionV2[cycle, step, :] + \
                                            velocity * oneArray
          
        time = time + deltaT
        tau = time * tauFac

    return


  def _timeCoeff(self, term, tau, aPrev, bPrev, factPrev):
    """
    Computes coefficients for term term and time tau.
    """
    tau0 = self.tau0
    if term == 0:
      factN = 1.0
      aN = 1.0 - math.exp(-tau)
      bN = (tau - aN)/tau0
    else:
      factN = term * factPrev
      aN = aPrev - tau**term * math.exp(-tau)/factN
      bN = bPrev - aN/tau0

    return aN, bN, factN
        
      
  def _u2A(self, tau):
    """
    Computes viscoelastic solution for times less than the recurrence time.
    """
    solutionU = numpy.zeros(self.numberPoints, dtype=numpy.float64)
    solutionV = numpy.zeros(self.numberPoints, dtype=numpy.float64)

    lockDepth = self.lockDepth.value
    tau0 = self.tau0
    velocity = self.velocity.value
    recurrenceTime = self.recurrenceTime.value

    for point in range(self.numberPoints):
      solution = (-0.5 * math.pi + \
                  numpy.arctan(self.points[point]/lockDepth))/tau0
      solutionU[point] = tau * solution
      solutionV[point] = solution
      aPrev = 0.0
      bPrev = 0.0
      factPrev = 1.0
      for term in range(self.numberTerms):
        aN, bN, factN = self._timeCoeff(term, tau, aPrev, bPrev, factPrev)
        solutionU[point] -= bN * self.pointCoeff[point, term]
        solutionV[point] -= aN * self.pointCoeff[point, term]/tau0
        aPrev = aN
        bPrev = bN
        factPrev = factN

    solutionU *= 2.0 * velocity * recurrenceTime/math.pi
    solutionV *= 2.0 * velocity * recurrenceTime/math.pi
    return [solutionU, solutionV]
        
      
  def _u2B(self, tau):
    """
    Computes viscoelastic solution for times greater than the recurrence time.
    """
    tau0 = self.tau0
    velocity = self.velocity
    recurrenceTime = self.recurrenceTime.value

    solutionU = numpy.zeros(self.numberPoints, dtype=numpy.float64)
    solutionV = numpy.zeros(self.numberPoints, dtype=numpy.float64)
    tau2 = tau - tau0

    for point in range(self.numberPoints):
      a1Prev = 0.0
      b1Prev = 0.0
      fact1Prev = 1.0
      a2Prev = 0.0
      b2Prev = 0.0
      fact2Prev = 1.0
      for term in range(self.numberTerms):
        a1N, b1N, fact1N = self._timeCoeff(term, tau, a1Prev, b1Prev, fact1Prev)
        a2N, b2N, fact2N = self._timeCoeff(term, tau2, a2Prev, b2Prev,
                                           fact2Prev)
        daDt = tau2**term * math.exp(-tau2)/fact2N
        solutionU[point] += self.pointCoeff[point, term] * \
                           (b2N - b1N + a2N)
        solutionV[point] += self.pointCoeff[point, term] * \
                            (a2N/tau0 - a1N/tau0 + daDt)
        a1Prev = a1N
        b1Prev = b1N
        fact1Prev = fact1N
        a2Prev = a2N
        b2Prev = b2N
        fact2Prev = fact2N

    solutionU *= 2.0 * velocity * recurrenceTime/math.pi
    solutionV *= 2.0 * velocity * recurrenceTime/math.pi
    return [solutionU, solutionV]
    
      
  def _writeSolution(self, solutionType):
    """
    Write solution a text file.
    """
    
    if solutionType == "dispacement":
      filename = self.dispfilename
      solution = self.solutionUTot
    else:
      filename = self.velfilename
      solution = self.solutionVTot

    from pyre.units.time import year

    f = open(filename, "w")
    f.write("dt = %f*year\n" % (self.deltaT.value/year.value,))
    f.write("dx = %s\n" % self.deltaX)
    f.write("ncycles = %d\n" % self.numberCycles)
    f.write("nsteps = %d\n" % (self.numberSteps+1,))
    f.write("npoints = %d\n" % self.numberPoints)
    data = solution.reshape( (self.numberCycles,
                              (self.numberSteps*1)*self.numberPoints) )
    numpy.savetxt(f, data, fmt="%14.6e")
    f.close()

    return


# ----------------------------------------------------------------------
if __name__ == '__main__':
  app = AnalyticalSoln()
  app.run()

# End of file
