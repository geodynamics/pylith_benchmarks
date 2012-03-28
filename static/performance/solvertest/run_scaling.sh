#!/bin/bash
#
# Shell script to facilitate running scaling benchmarks using cluster
# with PBS scheduler.

if [ $# == 2 ]; then
  cell=$1
  nprocs=$2
else
  echo "usage: run_scaling.sh CELL NPROCS"
  exit 1
fi

if [ $cell == "tet4" ] || [ $cell == "hex8" ]; then
  echo "do nothing" > /dev/null
else
  echo "Unknown cell '$cell'."
  exit 1
fi

pcfiles="fieldsplit_mult.cfg custompc.cfg"
args="--job.name=${cell}_np${nprocs} --job.stdout=${cell}_np${nprocs}.log"

if [ $nprocs == 1 ]; then
  pylith ${cell}.cfg ${cell}_np00${nprocs}.cfg $pcfiles $args --nodes=1 --scheduler.ppn=1

elif [ $nprocs == 2 ]; then
  pylith ${cell}.cfg ${cell}_np00${nprocs}.cfg $pcfiles $args --nodes=2 --scheduler.ppn=2

elif [ $nprocs == 4 ]; then
  pylith ${cell}.cfg ${cell}_np00${nprocs}.cfg $pcfiles $args --nodes=4 --scheduler.ppn=4

elif [ $nprocs == 8 ]; then
  pylith ${cell}.cfg ${cell}_np00${nprocs}.cfg $pcfiles $args --nodes=8 --scheduler.ppn=8

elif [ $nprocs == 16 ]; then
  pylith ${cell}.cfg ${cell}_np0${nprocs}.cfg $pcfiles $args --nodes=16 --scheduler.ppn=8

elif [ $nprocs == 32 ]; then
  pylith ${cell}.cfg ${cell}_np0${nprocs}.cfg $pcfiles $args --nodes=32 --scheduler.ppn=8

elif [ $nprocs == 64 ]; then
  pylith ${cell}.cfg ${cell}_np0${nprocs}.cfg $pcfiles $args --nodes=64 --scheduler.ppn=8

elif [ $nprocs == 128 ]; then
  pylith ${cell}.cfg ${cell}_np${nprocs}.cfg $pcfiles $args --nodes=128 --scheduler.ppn=8

else
  echo "Unknown number of processors '$nprocs'."
  exit 1
fi
