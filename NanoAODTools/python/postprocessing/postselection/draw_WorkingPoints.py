import os
import ROOT
import copy
from PhysicsTools.NanoAODTools.postprocessing.postselection.utils.loadHists import loadHists
import cmsstyle as CMS
import sys
import argparse
import json
sys.path.append('../')
ROOT.gROOT.SetBatch()

parser      = argparse.ArgumentParser(description='Collect histograms from different samples and save them into a single ROOT file.')
parser.add_argument('-e',   '--era',          type=str,               default='2023',             help='Era')
parser.add_argument(        '--TopCategory',  type=str,               default='Mixed',            help='Top Category: Resolved, Mixed, Merged')
parser.add_argument(        '--folder',       type=str,               default=None,               help='Folder of the WP production with plotsCollected.root (default: the one of the era in remoteFolderPath_dict); the pdf is saved here')
parser.add_argument(        '--outjson',      type=str,               default="./TopTagging_WorkingPoints.json", help='json where the WPs of <era>/<TopCategory> are written (created if missing, other eras/categories kept)')
args        = parser.parse_args()
TopCand     = args.TopCategory
era         = args.era
outFilePath = args.outjson

# Working points: name --> (key in the json, target mistag rate of nonmatched+other)
working_points = {
                    "L":    ("10%", 0.10),
                    "T":    ("5%",  0.05),
                    "XT":   ("1%",  0.01),
                }

if os.path.exists(outFilePath):
    print(f"Output file {outFilePath} exists. Loading it...")
    with open(outFilePath, 'r') as f:
        outDict = json.load(f)
else:
    print(f"Output file {outFilePath} does not exist. Will create it...")
    outDict                 = {}
if era not in outDict:
    outDict[era]            = {}
if TopCand not in outDict[era]:
    outDict[era][TopCand]   = {}

remoteFolderPath_dict = {
    "2022":         "/eos/user/l/lfavilla/RDF_DManalysis/TopTagging_WorkingPoints/2022/",
    "2022EE":       "/eos/user/l/lfavilla/RDF_DManalysis/TopTagging_WorkingPoints/2022EE/",
    "2023":         "/eos/user/l/lfavilla/RDF_DManalysis/TopTagging_WorkingPoints/run2023_March26_TaggerWorkingPoints/",
    "2023postBPix": "/eos/user/l/lfavilla/RDF_DManalysis/TopTagging_WorkingPoints/2023postBPix/",
    "2024":         "/eos/user/l/lfavilla/RDF_DManalysis/TopTagging_WorkingPoints/2024/"
    }

remoteFolderPath = args.folder if args.folder is not None else remoteFolderPath_dict[era]
inFilePath       = f"{remoteFolderPath}/plotsCollected.root"
if not os.path.exists(inFilePath):
    print(f"File {inFilePath} does not exist. Exiting...")
    exit(1)
else:
    # inFile       = ROOT.TFile.Open(inFilePath, "READ")
    histoDict    = loadHists(inFilePath)
print(histoDict.keys())
color_map        = {
                    "topmatched":   ROOT.TColor.GetColor("#5790fc"),
                    "nonmatched":   ROOT.TColor.GetColor("#e42536"),
                    "other":        ROOT.TColor.GetColor("#964a8b"),
                    }


var                  = f"BestTop{TopCand}_score"
title                = f"Best Top {TopCand} score"


####### Draw working points + cumulative distributions ####### 
CMS.SetExtraText("Private Work" + f" | {era} Top tagging WPs")
CMS.SetLumi("")
CMS.SetEnergy("")
CMS.ResetAdditionalInfo()
c                    = CMS.cmsCanvas(
                                        title,
                                        0.0,
                                        1.0,
                                        0.0,
                                        1.25,
                                        title,
                                        "1-cumulative",
                                        square=CMS.kRectangular,
                                        iPos=0
                                    )
# if TopCand == "Merged":
#     leg              = CMS.cmsLeg(0.57, 0.67, 0.87, 0.87, textSize=0.025) # Merged    
# elif TopCand == "Mixed":
#     leg              = CMS.cmsLeg(0.37, 0.47, 0.67, 0.67, textSize=0.025) # Mixed
# elif TopCand == "Resolved":
#     leg              = CMS.cmsLeg(0.67, 0.67, 0.87, 0.83, textSize=0.025) # Resolved
# leg              = CMS.cmsLeg(0.67, 0.72, 0.87, 0.87, textSize=0.025)
# leg1              = CMS.cmsLeg(0.67, 0.72, 0.87, 0.87, textSize=0.025)
leg1              = CMS.cmsLeg(0.77, 0.80, 0.92, 0.90, textSize=0.025)
leg2              = CMS.cmsLeg(0.37, 0.78, 0.57, 0.90, textSize=0.025)
# leg.AddEntry("None", f"{era} Top tagging WPs", "")

# With the fine binning (10000 bins) the markers would hide each other: the cumulatives are drawn as lines
nbins            = histoDict[f"{var}_BestTop{TopCand}_topmatched"].GetNbinsX()
use_lines        = nbins > 100

for i,proc in enumerate(color_map):
    histoName        = f"{var}_BestTop{TopCand}_{proc}"
    histo            = copy.deepcopy(histoDict[histoName])
    histo.Scale(1./histo.Integral())
    histo = histo.GetCumulative(forward=ROOT.kFALSE)
    if use_lines:
        CMS.cmsDraw(histo, "HIST", lcolor=color_map[proc], lwidth=2, fstyle=0)
        leg1.AddEntry(histo, proc, "L")
    else:
        CMS.cmsDraw(histo, "PE", mcolor=color_map[proc])
        leg1.AddEntry(histo, proc, "PE")

####### Find working points for topmatched and nonmatched+other #######
histo            = copy.deepcopy(histoDict[f"{var}_BestTop{TopCand}_nonmatched"])
histo.Add(copy.deepcopy(histoDict[f"{var}_BestTop{TopCand}_other"]))
histo.Scale(1./histo.Integral())
histo            = histo.GetCumulative(forward=ROOT.kFALSE)
if use_lines:
    CMS.cmsDraw(histo, "HIST", lcolor=ROOT.TColor.GetColor("#e76300"), lwidth=2, fstyle=0)
    leg1.AddEntry(histo, "nonmatched+other", "L")
else:
    CMS.cmsDraw(histo, "PE", mcolor=ROOT.TColor.GetColor("#e76300"))
    leg1.AddEntry(histo, "nonmatched+other", "PE")

histo_top        = copy.deepcopy(histoDict[f"{var}_BestTop{TopCand}_topmatched"])
histo_top.Scale(1./histo_top.Integral())
histo_top        = histo_top.GetCumulative(forward=ROOT.kFALSE)

# histo is the backward cumulative: bin i holds the fraction of background with score >= low edge of bin i,
# i.e. the mistag rate obtained by cutting at the low edge of bin i.
# WP = low edge of the FIRST bin whose mistag rate is below the target (10% for L, 5% for T, 1% for XT).
# The searches are independent, so two WPs can also fall in the same bin.
wp_bin = {wp: None for wp in working_points}
for i in range(1, histo.GetNbinsX()+1):
    mistag = histo.GetBinContent(i)
    for wp, (key, target) in working_points.items():
        if (mistag < target) and (wp_bin[wp] is None):
            wp_bin[wp] = i

for wp, (key, target) in working_points.items():
    if wp_bin[wp] is None:
        print(f"Mistag rate never goes below {key} for WP {wp} of {TopCand} (with {nbins} bins). Exiting...")
        exit(1)

thr     = {}
fpr     = {}
fpr_err = {}
tpr     = {}
for wp in working_points:
    thr[wp]     = histo.GetXaxis().GetBinLowEdge(wp_bin[wp])
    fpr[wp]     = histo.GetBinContent(wp_bin[wp])           # mistag rate at thr
    fpr_err[wp] = histo.GetBinError(wp_bin[wp])             # its statistical error
    tpr[wp]     = histo_top.GetBinContent(wp_bin[wp])       # top efficiency at thr

print("\n")
for wp, (key, target) in working_points.items():
    print(f"Working point {wp:2s} ({key:3s}): thr {thr[wp]:.4f} | nonmatched+other {100*fpr[wp]:.2f} +- {100*fpr_err[wp]:.2f}% | topmatched {100*tpr[wp]:.1f}%")
    outDict[era][TopCand][key]  = round(thr[wp], 4)
with open(outFilePath, 'w') as f:
    json.dump(outDict, f, indent=4)
print(f"Working points written in {outFilePath}")

wp_color = {
            "L":    ROOT.kRed,
            "T":    ROOT.kGreen+1,
            "XT":   ROOT.TColor.GetColor("#0033ff"),  # electric blue
            }
wp_lines = {}
for wp in working_points:
    wp_lines[wp] = ROOT.TLine(thr[wp], 0.0, thr[wp], 1.0)
    CMS.cmsDrawLine(wp_lines[wp], lcolor=wp_color[wp], lstyle=ROOT.kDashed)
    leg2.AddEntry(wp_lines[wp], f"WP_{{{wp}}} | thr: {thr[wp]:.4f} - tpr{100*tpr[wp]:.1f}% - fpr{100*fpr[wp]:.1f}%", "L")


# latex    = ROOT.TLatex()
# latex.SetTextFont(52)
# latex.SetTextSize(0.025)
# latex.SetTextColor(ROOT.kRed)
# if TopCand == "Merged":
#     latex.DrawLatexNDC(thr_L+0.1, 0.83, f"{thr_L:.3f}") # Merged
# elif TopCand == "Mixed":
#     latex.DrawLatexNDC(thr_L-0.05, 0.83, f"{thr_L:.3f}") # Mixed
# elif TopCand == "Resolved":
#     latex.DrawLatexNDC(thr_L-0.02, 0.83, f"{thr_L:.3f}") # Resolved

# latex    = ROOT.TLatex()
# latex.SetTextFont(52)
# latex.SetTextSize(0.025)
# latex.SetTextColor(ROOT.kGreen+1)
# if TopCand == "Merged":
#     latex.DrawLatexNDC(thr_T+0.02, 0.78, f"{thr_T:.3f}") # Merged
# elif TopCand == "Mixed":
#     latex.DrawLatexNDC(thr_T-0.02, 0.78, f"{thr_T:.3f}") # Mixed
# elif TopCand == "Resolved":
#     latex.DrawLatexNDC(thr_T-0.03, 0.78, f"{thr_T:.3f}") # Resolved


c.SaveAs(f"{remoteFolderPath}/{var}.pdf")