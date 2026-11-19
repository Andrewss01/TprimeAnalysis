import os
import ROOT
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import copy
import json
import argparse

parser = argparse.ArgumentParser(description='Collect histograms from different samples and save them into a single ROOT file.')
parser.add_argument('-e', '--era',          type=str,               default='2023',             help='Era')
parser.add_argument(      '--folder',       type=str,               default=None,               help='Folder of the WP production (default: the one of the era in remoteFolderPath_dict); plotsCollected.root and plotsCollected_counts.json are written here')
parser.add_argument(      '--plotsfolder',  type=str,               default=None,               help='Folder with the histograms of the samples (<sample>.root), e.g. <folder>/noTrotaSF/plots (default: <folder>/plots, layout of the old productions)')
args   = parser.parse_args()
era    = args.era


remoteFolderPath_dict = {
    "2022":         "/eos/user/l/lfavilla/RDF_DManalysis/TopTagging_WorkingPoints/2022/",
    "2022EE":       "/eos/user/l/lfavilla/RDF_DManalysis/TopTagging_WorkingPoints/2022EE/",
    "2023":         "/eos/user/l/lfavilla/RDF_DManalysis/TopTagging_WorkingPoints/run2023_March26_TaggerWorkingPoints/",
    "2023postBPix": "/eos/user/l/lfavilla/RDF_DManalysis/TopTagging_WorkingPoints/2023postBPix/",
    "2024":         "/eos/user/l/lfavilla/RDF_DManalysis/TopTagging_WorkingPoints/2024/"
    }


remoteFolderPath = args.folder if args.folder is not None else remoteFolderPath_dict[era]
plotsFolderPath  = args.plotsfolder if args.plotsfolder is not None else f"{remoteFolderPath}/plots"
if not os.path.isdir(plotsFolderPath):
    print(f"Plots folder {plotsFolderPath} does not exist: give the folder with the <sample>.root histograms with --plotsfolder. Exiting...")
    exit(1)
print(f"Reading sample histograms from {plotsFolderPath}")
outFilePath      = f"{remoteFolderPath}/plotsCollected.root"
countFilePath    = f"{remoteFolderPath}/plotsCollected_counts.json"


TopCategories    = [
                    "Resolved",
                    "Mixed",
                    "Merged"
                    ]

datasets         = [
                      f"TT_{era}",
                      f"TW_{era}",
                      f"QCD_{era}",
                    #   f"ZJetsToNuNu_2jets_{era}",
                    #   f"WJets_2jets_{era}",
                    ]

processes_map      = {
                    "topmatched":   ["TT", "TW"],
                    "nonmatched":   ["TT", "TW"],
                    "other":        ["QCD", "ZJetsToNuNu", "WJets"],
                    }

samples_list        = []
for dat in datasets:
    sample          = sample_dict[dat]
    if hasattr(sample, "components"):
        samples_list.extend(sample.components)
    else:
        samples_list.append(sample)

# All the samples are needed: a missing one would change the TT/TW/QCD mix, and so the WPs, without notice.
# Checked before writing anything, so that a wrong folder never overwrites plotsCollected.root
missing_files       = [f"{plotsFolderPath}/{s.label}.root" for s in samples_list if not os.path.exists(f"{plotsFolderPath}/{s.label}.root")]
if len(missing_files) > 0:
    print(f"{len(missing_files)} sample files missing in {plotsFolderPath}:")
    for f in missing_files:
        print(f"  {f}")
    print("Exiting...")
    exit(1)

plotsDict                           = {topCand: {proc: None for proc in processes_map} for topCand in TopCategories}
countDict                           = {topCand: {proc: 0 for proc in processes_map} for topCand in TopCategories}
for topCand in TopCategories:
    for proc in processes_map:
        variable                        = f"BestTop{topCand}_score"
        region                          = f"BestTop{topCand}_{proc}"
        histoName                       = f"{variable}_{region}"

        for s in samples_list:
            if s.process.split("_")[0] in processes_map[proc]:
                inFilePath              = f"{plotsFolderPath}/{s.label}.root"
                inFile                  = ROOT.TFile.Open(inFilePath, "READ")
                histo                   = copy.deepcopy(ROOT.TH1D(inFile.Get(histoName)))
                print(f"Processing histo {histoName} file: {s.label} with {histo.Integral()} integral")
                if plotsDict[topCand][proc] is None:
                    plotsDict[topCand][proc]     = histo
                else:
                    plotsDict[topCand][proc].Add(histo)
                countDict[topCand][proc] += histo.Integral()

with open(countFilePath, "w") as f:
    json.dump(countDict, f, indent=4)
print(f"Saved counts to {countFilePath}")


print(f"Writing output file {outFilePath}")
outFile = ROOT.TFile.Open(outFilePath, "RECREATE")
for topCand in plotsDict:
    for proc in plotsDict[topCand]:
        if plotsDict[topCand][proc] is not None:
            plotsDict[topCand][proc].Write()
outFile.Close()