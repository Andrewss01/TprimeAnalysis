#!/bin/bash

for mt in $(seq 700 100 1800); do
   echo "==> Launching MT=${mt}"
   python3 postSelector_submitter.py -d "TprimeToTZ_${mt}_2022" --syst --wp "_WP5"
done

# for mt in $(seq 700 100 1800); do
#     echo "==> Launching MT=${mt}"
#     python3 postSelector_submitter.py -d "TprimeToTZ_${mt}_2022" --syst --wp "_WP1" --trota2d
# done


# python3 postSelector_submitter.py -d ZJetsToNuNu_2jets_2022 --syst --trota2d --wp "_WP1"
python3 postSelector_submitter.py -d ZJetsToNuNu_2jets_2022 --syst  --wp "_WP5"
