These scripts can be used to calibrate a SiPM with the LED pulser.

The first step is to calibrate the LED itself.

These scripts analyze several Janus data files from an LED study in which you have scanned driving voltage. plotGauss_LED fits
energy distributions from one channel to a Gaussian distribution and writes the mean and
the gain setting to a csv file. GainScan.py analyzes this CSV file and plots a curve, gain
factor vs gain setting, producing a new csv file (these are saved in a directory called
DataFiles).

The next step is to study a SiPM with the calibrated LED.

You could easily modify these scripts for any other study where you scan one parameter (e.g.,
bias voltage).

The bas script gainstudies.sh iterates over several Janus data files, automatically running
plotRunPHA.py and plotGauss_GS.py. After it's done, you should then run GainScan.py to
produce the gain factor vs. gain setting curve.
