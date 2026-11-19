####################################################################################################
# How to use postSelector_submitter_large.py
#
# ### ==> Modes (-m, set with OPT below):
# -m s --> submits the jobs (one condor job per part of --partsize root files)
# -m c --> checks the jobs: prints ok / failed / still in the queue and "total to rerun"
# -m r --> resubmits the failed jobs (the ones still in the queue are skipped)
# -m h --> merges the parts: <OUTPATH>/<weightset>/parts/<sample>_partN.root -> <MERGEPATH>/<weightset>/plots/<sample>.root
#          (hadd of a local copy in /tmp, the merged file is copied back and checked; the parts are never removed)
# -m d --> removes the parts, only after checking them against the merged file already in <MERGEPATH>/<weightset>/plots/
#          (no new hadd); use it as the very last step: after it, -m c/r see the removed parts as failed jobs
# Samples with a single part are written directly in <OUTPATH>/<weightset>/plots/
#
# ### ==> Sequence of operations:
# s --> c (and r) until the queue is empty and "total to rerun: 0" --> h --> d
# Use the SAME options in every mode, only OPT changes: e.g. -m h without the --noXXX/--weightset options
# of the submission looks for the parts in another weightset folder and does not find them
#
# ### ==> Weightsets (which weights enter the event weight):
# --noSFbtag, --noPuWeight, --noTopPtWeight, --noTrotaSF   remove that weight from every weightset
# --weightset X (repeatable)                              adds one weightset, X = allWeights or the weights to remove
#                                                         separated by commas, e.g. --weightset noSFbtag,noPuWeight
# Each weightset has its own folder <OUTPATH>/<label>/, label = removed weights joined by _ (allWeights if none),
# e.g. "--noTrotaSF --weightset allWeights --weightset noSFbtag" -> noTrotaSF/ and noSFbtag_noTrotaSF/
# No --weightset and no --noXXX: a single weightset, allWeights/
#
# ### ==> Paths:
# --outpath   folder of the job outputs (parts/ of the split samples)
# --mergepath folder of the merged files (plots/), i.e. the one used for the stacks; same as --outpath if not given
#
# ### ==> Other options:
# --varfile    variables and regions (default ../variables.py)
# --syst       systematic variations (MC only, not for data)
# --config_paths, --dict_samples_file   other config / samples file
# --dryrun     only prepares the condor folders;  --verbose N   extra printouts
#
# The standalone environment (standalone/env_standalone.sh) must already be sourced.
# Below: an example for one year, change the variables at the top.
####################################################################################################

export OPT=s                                            # s, c, r, h, d
export YEAR=2024
export RUN=run${YEAR}_Example                           # name of the production
export OUTPATH=/eos/user/<initial>/<user>/<folder>/${YEAR}/${RUN}/
export MERGEPATH=${OUTPATH}
export VARFILE=../variables.py
export PARTSIZE=10
export WEIGHTS="--noTrotaSF"                            # weightsets, see above

export COMMON="--suffix ${RUN} --partsize ${PARTSIZE} --outpath ${OUTPATH} --mergepath ${MERGEPATH} --varfile ${VARFILE} ${WEIGHTS}"

### Samples
MC="TT_${YEAR},TW_${YEAR},QCD_${YEAR},ZJetsToNuNu_2jets_${YEAR},WJets_2jets_${YEAR}"
SIGNAL_MASSES="700 800 900 1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000 2200 2400 2600"   # T' -> tZ, masses available in the samples file of the year
SIGNAL=""
for m in ${SIGNAL_MASSES}; do
    SIGNAL="${SIGNAL}TprimeToTZ_${m}_${YEAR},"
done
SIGNAL=${SIGNAL%,}
DATA="DataJetMET_${YEAR}"

### Background MC, signal (with --syst) and data (no --syst)
python3 postSelector_submitter_large.py -m ${OPT} -d ${MC}     --syst ${COMMON}
python3 postSelector_submitter_large.py -m ${OPT} -d ${SIGNAL} --syst ${COMMON}
python3 postSelector_submitter_large.py -m ${OPT} -d ${DATA}          ${COMMON}

### Other samples, if needed
# python3 postSelector_submitter_large.py -m ${OPT} -d DataEGamma_${YEAR} ${COMMON}
# python3 postSelector_submitter_large.py -m ${OPT} -d DataMuon_${YEAR} ${COMMON}
# python3 postSelector_submitter_large.py -m ${OPT} -d TBDM_s_${YEAR},TBDM_ps_${YEAR},TTDM_s_${YEAR},TTDM_ps_${YEAR},TWDM_s_${YEAR},TWDM_ps_${YEAR} --syst ${COMMON} --dict_samples_file ../samples/dict_samples_${YEAR}_tdm.json
