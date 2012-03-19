#!/bin/bash

if [ $# == 1 ]; then
  sims=$1
else
  sims="all"
fi

# ----------------------------------------------------------------------
if [ $sims == "all" ] || [ $sims == "asm" ]; then
  # ASM
  #
  # STATUS: OK
  echo "ASM preconditioner"
  pylith tet4.cfg asm.cfg >& tet4_asm.log
  pylith hex8.cfg asm.cfg >& hex8_asm.log
fi

# ----------------------------------------------------------------------
if [ $sims == "all" ] || [ $sims == "fieldsplit" ]; then

  # field split, additive
  #
  # STATUS: OK
  echo "field split, additive"
  pylith tet4.cfg fieldsplit_add.cfg >& tet4_fieldsplit_add.log
  pylith hex8.cfg fieldsplit_add.cfg >& hex8_fieldsplit_add.log

  # field split, multiplicative
  #
  # STATUS: OK
  echo "field split, multiplicative"
  pylith tet4.cfg fieldsplit_mult.cfg >& tet4_fieldsplit_mult.log
  pylith hex8.cfg fieldsplit_mult.cfg >& hex8_fieldsplit_mult.log

  # field split, multiplicative w/custom fault preconditioner
  #
  # STATUS: OK
  echo "field split, multiplicative w/custom pc"
  pylith tet4.cfg fieldsplit_mult.cfg custompc.cfg >& tet4_fieldsplit_mult_custompc.log
  pylith hex8.cfg fieldsplit_mult.cfg custompc.cfg >& hex8_fieldsplit_mult_custompc.log

fi

# ----------------------------------------------------------------------
if [ $sims == "all" ] || [ $sims == "schur" ]; then

  # Schur complement, diagonal
  #
  # STATUS: BUG, hangs at very beginning of solve for tet4 
  #              true residual does not decrease for hex8
  echo "schur, diag"
  pylith tet4.cfg schur_diag.cfg >& tet4_schur_diag.log
  pylith hex8.cfg schur_diag.cfg >& hex8_schur_diag.log

  # Schur complement, lower
  #
  # STATUS: BUG, hangs at very beginning of solve for tet4 
  #              hangs at iteration 8 for hex8
  echo "schur, lower"
  pylith tet4.cfg schur_lower.cfg >& tet4_schur_lower.log
  pylith hex8.cfg schur_lower.cfg >& hex8_schur_lower.log

  # Schur complement, upper
  #
  # STATUS: BUG, hangs at very beginning of solve for tet4 
  #              works for hex8
  echo "schur, upper"
  pylith tet4.cfg schur_upper.cfg >& tet4_schur_upper.log
  pylith hex8.cfg schur_upper.cfg >& hex8_schur_upper.log

  # Schur complement, full
  #
  # STATUS: BUG, hangs at very beginning of solve for tet4 
  #              works for hex8
  echo "schur, full"
  pylith tet4.cfg schur_full.cfg >& tet4_schur_full.log
  pylith hex8.cfg schur_full.cfg >& hex8_schur_full.log

fi
