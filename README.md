# Python Module for Simulating OTR Light
Code Status: working, but very incomplete!

## Changes:
Now, pyOTR is written in a "vectorized" way and it uses parallel computing.
Instead of computing the path of each ray of light individually, it now
uses Linear Algebra to compute the path of many rays at once and it
divided the total number of rays into chuncks of data that are ran in parallel.

The gain in speed is very substantial:     
In the original version, it took ~20 s to generate and trace the path of 100,000 rays.    
Now, it takes less than 2 s and 1,000,000 rays can be traced in 20 s!

## Usage:
python pyOTR.py

