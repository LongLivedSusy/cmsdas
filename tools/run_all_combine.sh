#!/bin/bash

new_dir="limits_v4"
json_file="limits.json"

# make directory (only if it does not already exist)
mkdir --parents $new_dir

# copy background root file
cp totalweightedbkgsDataDrivenMC.root $new_dir

cd $new_dir

# decay lengths (ctau) to loop over
declare -a decay_lengths=("10" "30" "100" "1000")

for ctau in "${decay_lengths[@]}"
do
    # copy skim root file
    cp ../skim_g1800_chi1400_27_200970_step4_"$ctau".root .

    # run prepinput.py
    python ../prepinput.py "$ctau"
    
    # run mkdcard.py
    python ../mkdcard.py distrack_"$ctau"_datacard_input.root
    
    # run combine
    combine -m "$ctau" -M AsymptoticLimits distrack_"$ctau"_datacard_input.txt > ctau"$ctau"_limit.txt

done

../../../CombineHarvester/CombineTools/scripts/combineTool.py -M CollectLimits higgsCombineTest.AsymptoticLimits.*.root $json_file

echo "Complete! Please use $new_dir/$json_file for plots."


