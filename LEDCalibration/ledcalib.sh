let i=0
for run in {5131..5156}
do
        python3 ../plotRunPHA.py $run 01 -l -q -b #for board 1: the EMCal board
	python3 plotGauss_LED.py 02 $run $i
	let i+=1
done

#LED study of ND filter 1 stop: {5131..5156}

#led calibration: {4341..4349} {4354..4394}
