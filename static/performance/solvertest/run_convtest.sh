#!/bin/bash

for ver in hex8 tet4; do

  # Small tolerance w/ASM
  sim=${ver}_smalltol
  pylith hex8.cfg asm.cfg --petsc.ksp_rtol=1.0e-18 >& ${sim}.log
  cd output; changeprefix hex8 ${sim}; cd ../

  # Field split w/custom, PC rtol=1.0e-6
  sim=${ver}_tol6
  pylith hex8.cfg fieldsplit.cfg custompc.cfg --petsc.ksp_rtol=1.0e-6  >& ${sim}.log
  cd output; changeprefix hex8 ${sim}; cd ../

  # Field split w/custom, PC rtol=1.0e-7
  sim=${ver}_tol7
  pylith hex8.cfg fieldsplit.cfg custompc.cfg --petsc.ksp_rtol=1.0e-7  >& ${sim}.log
  cd output; changeprefix hex8 ${sim}; cd ../

  # Field split w/custom, PC rtol=1.0e-8
  sim=${ver}_tol8
  pylith hex8.cfg fieldsplit.cfg custompc.cfg --petsc.ksp_rtol=1.0e-8  >& ${sim}.log
  cd output; changeprefix hex8 ${sim}; cd ../

done

