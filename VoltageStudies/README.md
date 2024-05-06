These scripts analyze several Janus data files from a bias scan study. plotGauss_VS fits
energy distributions from one channel to a Gaussian distribution and writes the mean and
the gain setting to a csv file. VoltageScan.py analyzes this CSV file and plots a curve, gain
factor vs overvoltage, producing a new csv file (these are saved in a directory called
DataFiles).

You could easily modify these scripts for any other study where you scan one parameter (e.g.,
bias voltage).

The bash script gainstudies.sh iterates over several Janus data files, automatically running
plotRunPHA.py and plotGauss_VS.py. After it's done, you should then run VoltageScan.py to
produce the gain factor vs. gain setting curve.