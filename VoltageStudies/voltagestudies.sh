let i=0 #first voltage setting: 0.5 V below recommended
for run in {3135..3185}
do
        let i+=1 #in this study I incremented voltage by 0.05 V each run
        python3 ~/EMCal_analysis/plotRunPHA.py $run -l -q -b
	python3 ~/EMCal_analysis/VoltageStudies/plotGauss_VS.py 00,01,02,03 $run $i,$i,$i,$i
done
