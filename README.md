# Python Module for Simulating OTR Light

## To Do:    
- (Done!)   Vectorize the calculations
- (Done!)   Parallelize
- (Partial) Implement all Foils
-           Implement Mirrors
-           Implement Camera

## Updates:
Jan 22nd:    
Now, pyOTR is written in a "vectorized" way and it uses parallel computing.
Instead of computing the path of each ray of light individually, it now
uses Linear Algebra to compute the path of many rays at once and it
divided the total number of rays into chuncks of data that are ran in parallel.

The gain in speed is very substantial:     
In the original version, it took ~20 s to generate and trace the path of 100,000 rays.    
Now, it only takes less than 2 s and 20 s can not trace 1,000,000 rays!!

## Configuration:
The definitions of all necessary parameters to set up the simulation are in the Config.py Module.    
The main ones to change right now are:

### VERBOSE (default: 0):
Set it to 1 to include debugging info.

### nrays:
Number of photons to be simulated

### xmax:
Size of initial square side to randomly generate the photons.

## Usage:
python pyOTR.py

The jupyter notebook "Examples" shows a few plots of the distribution of photons before and after passing by the Calibration Foil.