import ROOT 
import cmsstyle as CMS
import os, sys
from variables import *
from samples.samples import *
import numpy as np
import json
import math
import copy
import yaml
import argparse
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

parser          = argparse.ArgumentParser()
parser.add_argument("--era", dest="era", type=str, default="2023", help="Please enter the era, e.g. 2022, 2022EE, etc.")
parser.add_argument("--folder", dest="folder", type=str, default=None, help="triggerSF results folder with plots/ inside, ending with '/' (default: config['outputfolder']['triggerSF_results'][era])")
args            = parser.parse_args()
era             = args.era
year            = 0
if "2022" in era:
    year        = "2022"
elif "2023" in era:
    year        = "2023"
elif "2024" in era:
    year        = "2024"

def cms_canvas_1D(canv_name, x_min, x_max, y_min, y_max, xtitle, ytitle, iPos=11):
    # cmsCanvas (rectangular, 800x600) with more room for the axis labels: with the cmsstyle margins the y title overlaps
    # the tick labels and the last x label (1000) is cut by the right edge of the canvas
    canv = CMS.cmsCanvas(canv_name, x_min, x_max, y_min, y_max, xtitle, ytitle, square=CMS.kRectangular, extraSpace=0.04, iPos=iPos, yTitOffset=1.05)
    canv.SetRightMargin(0.05)
    # the CMS and lumi texts (TLatex) were placed with the old right margin: remove them and draw them again
    for obj in list(canv.GetListOfPrimitives()):
        if obj.InheritsFrom("TLatex"):
            canv.GetListOfPrimitives().Remove(obj)
    CMS.CMS_lumi(canv, iPos)
    hdf = CMS.GetcmsCanvasHist(canv)
    for axis in [hdf.GetXaxis(), hdf.GetYaxis()]:
        axis.SetLabelSize(0.045)
        axis.SetTitleSize(0.055)
    return canv

def save_pdf(canv, path, close=True):
    # pdf page with the same proportions as the canvas (cmsstyle sets a 20x20 cm paper: white space around the plot,
    # and the wide canvases were shifted and cut); the longer side is 28 cm, ROOT caps the pdf page at ~29.7 cm (A4)
    ratio = canv.GetWw() / canv.GetWh()
    if ratio >= 1:
        ROOT.gStyle.SetPaperSize(28., 28. / ratio)
    else:
        ROOT.gStyle.SetPaperSize(28. * ratio, 28.)
    CMS.SaveCanvas(canv, path, close=close)

def plot(h, folder, fillcolor, canv_name = "canv" ,extraTest="Preliminary", iPos=0, energy="13", lumi = "",  addInfo="", ytitle = "Efficiency"):

    if type(h)==list:
        h1 = h[0]
        # hist_dict = [k.GetName() for k in h]
    else:
        h1 = h
    CMS.SetExtraText(extraTest)
    iPos = iPos
    canv_name = canv_name
    CMS.SetLumi(lumi)
    CMS.SetEnergy(energy)
    CMS.ResetAdditionalInfo()
    CMS.AppendAdditionalInfo(addInfo)

    x_min = h1.GetXaxis().GetXmin()
    x_max = h1.GetXaxis().GetXmax()
    y_min = h1.GetMinimum()
    if y_min !=0: y_min = y_min - 0.2
    y_max = h1.GetMaximum()
    y_max = y_max + 0.3 * (y_max - y_min)
    x_axis_name = h1.GetXaxis().GetTitle()
    canv = cms_canvas_1D(canv_name, x_min, x_max, y_min, y_max, x_axis_name, ytitle, iPos=iPos)
    hdf = CMS.GetcmsCanvasHist(canv)
    hdf.GetYaxis().SetMaxDigits(1)
    # Shift multiplier position
    ROOT.TGaxis.SetExponentOffset(-0.10, 0.01, "Y")
    leg = CMS.cmsLeg(0.5, 0.1, 0.98, 0.5, textSize=0.04)
    if type(h)==list:
        CMS.cmsDraw(h[1], "P", marker= 8, lcolor =  ROOT.TColor.GetColor("#e42536"), mcolor =  ROOT.TColor.GetColor("#e42536"))
        leg.AddEntry(h[1], "Simulation", "l")
        CMS.cmsDraw(h[0], "P", marker= 8, lcolor = ROOT.kBlack, mcolor = ROOT.kBlack)
        leg.AddEntry(h[0], "Data", "l")
        leg.Draw("same")
    else:
        if ytitle=="SF":
            CMS.cmsDraw(h1, "P", marker= 8 , mcolor = fillcolor)
        else:
            CMS.cmsDraw(h1, "P", marker= 8 ,lcolor = fillcolor, mcolor = fillcolor)
    save_pdf(canv, folder+"/pdf/1D/"+canv_name+".pdf")
    # CMS.SaveCanvas(canv, folder+"/png/"+canv_name+".png")
    # CMS.SaveCanvas(canv, folder+"/C/"+canv_name+".C")

def plot2D(h1, folder, v, canv_name = "canv2d" ,extraTest="Simulation", iPos=0, energy="13", lumi = "",  addInfo="", ztitle="Efficiency"):

    CMS.SetExtraText(extraTest)
    iPos = iPos
    canv_name = canv_name
    CMS.SetLumi(lumi)
    CMS.SetEnergy(energy)
    CMS.ResetAdditionalInfo()
    CMS.AppendAdditionalInfo(addInfo)

    x_min = v._xarray[0]
    x_max = v._xarray[-1]
    y_min = v._yarray[0]
    y_max = v._yarray[-1]
    x_axis_name = v._xtitle
    y_axis_name = v._ytitle
    canv = CMS.cmsCanvas(canv_name,x_min,x_max, y_min ,y_max,x_axis_name,y_axis_name,square=CMS.kSquare,extraSpace= 0.01, iPos=iPos, with_z_axis=True)
    ROOT.gStyle.SetPaintTextFormat("1.4f")
    h1.Draw("same colz text50 e")
    h1.GetZaxis().SetMaxDigits(2)
    h1.GetZaxis().SetTitle(ztitle)
    h1.GetZaxis().SetTitleOffset(1.35)
    h1.GetZaxis().SetTitleSize(0.035)
    h1.GetZaxis().SetLabelSize(0.035)
    h1.GetZaxis().SetLabelOffset(0.005)

    hdf = CMS.GetcmsCanvasHist(canv)
    hdf.GetYaxis().SetMaxDigits(2)
    hdf.GetYaxis().SetLabelSize(0.045)
    hdf.GetXaxis().SetLabelSize(0.045)
    hdf.GetXaxis().SetLabelOffset(0.005)
    hdf.GetYaxis().SetLabelOffset(0.005)
    hdf.GetXaxis().SetTitleOffset(1.3)
    hdf.GetYaxis().SetTitleOffset(1.3)
    hdf.GetXaxis().SetTitleSize(0.045)
    hdf.GetYaxis().SetTitleSize(0.045)
    # Shift multiplier position
    ROOT.TGaxis.SetExponentOffset(-0.10, 0.01, "Y")

    # Set the CMS official palette
    CMS.SetCMSPalette()
    CMS.UpdatePalettePosition(h1, canv)
    
    save_pdf(canv, folder+"/pdf/2D/"+canv_name+".pdf")
    # CMS.SaveCanvas(canv, folder+"/png/"+canv_name+".png")
    # CMS.SaveCanvas(canv, folder+"/C/"+canv_name+".C")

cut  = requirements  ### defined in variables.py 
config = {}
config_paths = os.environ.get('PWD')+'/config/config.yaml'
if os.path.exists(config_paths):
    with open(config_paths, "r") as _f:
        config = yaml.safe_load(_f) or {}
    print(f"Loaded config file from {config_paths}")
else:
    print(f"Config file not found in {config_paths}, exiting")
    sys.exit(1)

lumi_dict                           = config["plotting"]["lumi_dict"]
lumi_dict["Full2022"]               = lumi_dict["2022"] + lumi_dict["2022EE"]
lumi_dict["Full2023"]               = lumi_dict["2023"] + lumi_dict["2023postBPix"]
lumi_dict["Full2022_Full2023"]      = lumi_dict["Full2022"] + lumi_dict["Full2023"]
lumi = lumi_dict[era]  # in fb
run2 = False
run3 = not run2

datasets = [
    f"DataEGamma_{era}",
    f"TT_{era}",
    f"QCD_{era}",
    f"ZJetsToNuNu_2jets_{era}",
    f"WJets_2jets_{era}"
    ]
if len(datasets) > 2:
    plotname = ""
else:
    if "TT" in datasets[1]:
        plotname = "_ONLYTT"
    elif "ZJets" in datasets[1]:
        plotname = "_ONLYZJets"
    elif "WJets" in datasets[1]:
        plotname = "_ONLYWJets"

for d in datasets:
    if hasattr(sample_dict[d], "components"):
        components = sample_dict[d].components
    else:
        components = [sample_dict[d]]


blind = False # Set to True if you want to blind the data


# Specify the path to the JSON file
dict_samples_file   = config["dict_samples"][year].replace("..", os.environ.get('PWD'))
with open(dict_samples_file, "r") as file:
    samples = json.load(file)

print("Paremeters setted") 
print("cut              = {}".format(cut))      
print("lumi (fb)        = {}".format(str(lumi)))
print("input datasets   = {}".format([sample_dict[d].label for d in datasets]))
# print("blind            = {}".format(blind))

################# variables & regions definition --> defined in variables.py 
# print("Producing histos:  {}".format([v._name for v in vars[1:]]))
# print("Regions:           {}".format(regions.keys()))

############### out folders  
if args.folder is not None:
    folder  = args.folder
else:
    folder  = config["outputfolder"]["triggerSF_results"][era]
if not folder.endswith("/"):
    print(f"--folder must end with '/': {folder}, exiting")
    sys.exit(1)

if not os.path.exists(folder):
    os.mkdir(folder)
repohisto = folder+"plots/"
if not os.path.exists(repohisto):
    os.mkdir(repohisto)
repostack = folder+"stacks/"
if not os.path.exists(repostack):
    os.mkdir(repostack)
if not os.path.exists(repostack+"/png"):
    os.mkdir(repostack+"/png")
if not os.path.exists(repostack+"/pdf"):
    os.mkdir(repostack+"/pdf")
for subfolder in ["1D", "2D"]:     # 1D plots (curves vs MET) and 2D maps in separate subfolders
    os.makedirs(repostack+"/pdf/"+subfolder, exist_ok=True)
if not os.path.exists(repostack+"/C"):
    os.mkdir(repostack+"/C")

print("Created folders 'plots' and 'stacks' at ", folder)

################### utils ###################
def cut_string(cut):
    return cut.replace(" ", "").replace("&&","_").replace(">","_g_").replace(".","_").replace("==","_e_").replace("<", "_l_")

var = []
var.append(variable(name = "PuppiMET_pt", title= "p_{T}^{miss}(Puppi) [GeV]", nbins = 8, xmin = 100, xmax=800))
var.append(variable(name = "PuppiMET_phi", title= "MET #phi (Puppi) [GeV]", nbins = 6, xmin = -math.pi, xmax=math.pi))
var.append(variable(name = "PuppiMET_T1_pt_nominal", title= "p_{T}^{miss}(Puppi) [GeV]", nbins = 12, xarray = np.array([100, 125, 150, 175, 200, 225, 250, 275, 300, 350, 400, 500, 1000], dtype = 'd')))#,xmin = 100, xmax=800))
var.append(variable(name = "MHT", title= "MHT [GeV]", nbins = 6, xarray = np.array([0, 100, 200, 300, 400, 500, 1000], dtype = 'd')))#,xmin = 100, xmax=800))
var.append(variable(name = "PuppiMET_T1_phi_nominal", title= "Puppi MET #phi nominal", nbins = 6, xmin = -math.pi, xmax=math.pi))
var.append(variable(name = "nJet", title= "# Jet", nbins = 10, xmin = -0.5, xmax=9.5))
var.append(variable(name = "nFatJet", title= "# FatJet", nbins = 5, xmin = -0.5, xmax=4.5))
var.append(variable(name = "LeadingElectronPt_pt", title= "Leading Electron p_{T} [GeV]", nbins = 30, xmin = 0, xmax=300))
var2d = [] 
# var2d.append(variable2D(name = "PuppiMET_T1_pt_nominalVsMHT", xname = "PuppiMET_T1_pt_nominal", yname = "MHT", xtitle = "p_{T}^{miss}(Puppi) [GeV]", ytitle = "MHT [GeV]", nxbins = 12, xarray = np.array([100, 125, 150, 175, 200, 225, 250, 275, 300, 350, 400, 500, 1000], dtype = 'd'),  nybins = 6, yarray = np.array([0, 100, 200, 300, 400, 500, 1000], dtype = 'd')))

hlt_met = "(HLT_PFMET120_PFMHT120_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)"
hlt_ele = "(HLT_Ele32_WPTight_Gsf || HLT_Ele115_CaloIdVT_GsfTrkIdT || HLT_Photon200)"

regions = {
    "orthogonalPreselR_Ntot"     :  hlt_ele +" && PuppiMET_T1_pt_nominal>100 && nTightElectron>0",
    "orthogonalPreselR_Npass"    :  hlt_ele+" && "+ hlt_met +" && PuppiMET_T1_pt_nominal>100 && nTightElectron>0",
    "orthogonalPreselR2_Ntot"     :  hlt_ele +" && PuppiMET_T1_pt_nominal>100 && nTightElectron>0",
    "orthogonalPreselR2_Npass"    :  hlt_ele+" && "+ hlt_met +" && PuppiMET_T1_pt_nominal>100 && MinDelta_phi>0.6 && nTightElectron>0",
    "orthogonalPreselR_CR"       :  hlt_ele+" && "+ hlt_met +" && PuppiMET_T1_pt_nominal>100 && MinDelta_phi>0.6 && nTightElectron==0"
}

infile      = {'Data': [], 'signal': [], 'bkg': []}
infile2D      = {'Data': [], 'signal': [], 'bkg': []}
insample    = {'Data': [], 'signal': [], 'bkg': []}

cut_tag     = cut_string(cut)

for dat in datasets:
    d = sample_dict[dat]
    # print(repohisto + d.label + ".root")
    if hasattr(d, 'components'):
        s_list = d.components
    else:
        s_list = [d]

    for s in s_list:
        if 'Data' in s.label:
            infile['Data'].append(ROOT.TFile.Open(repohisto + s.label + ".root"))
            insample['Data'].append(s)
            if len(var2d)>0:
                infile2D['Data'].append(ROOT.TFile.Open(repohisto + s.label + "_2D.root"))
        else:
            infile['bkg'].append(ROOT.TFile.Open(repohisto + s.label + ".root"))
            insample['bkg'].append(s)
            if len(var2d)>0:
                infile2D['bkg'].append(ROOT.TFile.Open(repohisto + s.label + "_2D.root"))
    
h_bkg_total    = None
h_data_total   = None
h_bkg_pass     = None
h_data_pass    = None


outfileroot = ROOT.TFile.Open(repohisto + "TriggerEfficiency.root", "RECREATE")

for v in [var[2]]:
    r = "orthogonalPreselR_Ntot"
    for i, (f,s) in enumerate(zip(infile["bkg"], insample["bkg"])):
        histo_name = v._name+"_"+r
        tmp = copy.deepcopy(ROOT.TH1D(f.Get(histo_name)))
        if len(samples[s.label][s.label]["ntot"]):
            # tmp.Scale(s.sigma*(10**3)*lumi/np.sum(samples[s.label][s.label]["ntot"]))
            tmp.Scale(lumi)
        else:
            continue
        tmp.SetTitle("")
        if h_bkg_total==None:
            h_bkg_total = tmp.Clone("")
            h_bkg_total.SetName(v._name+"_"+r+"_bkgtotal")
        else:
            h_bkg_total.Add(tmp)
        
    for f, s in zip(infile["Data"], insample["Data"]):
        histo_name = v._name+"_"+r
        tmp = copy.deepcopy(ROOT.TH1D(f.Get(histo_name)))
        tmp.SetTitle("")
        if h_data_total==None:
            h_data_total = tmp.Clone("")
            h_data_total.SetName(v._name+"_"+r+"_datatotal")
        else:
            h_data_total.Add(tmp)

    r = "orthogonalPreselR_Npass"
    for i, (f,s) in enumerate(zip(infile["bkg"], insample["bkg"])):
        histo_name = v._name+"_"+r
        tmp = copy.deepcopy(ROOT.TH1D(f.Get(histo_name)))
        if len(samples[s.label][s.label]["ntot"]):
            # tmp.Scale(s.sigma*(10**3)*lumi/np.sum(samples[s.label][s.label]["ntot"]))
            tmp.Scale(lumi)
        else:
            continue
        tmp.SetTitle("")
        if h_bkg_pass==None:
            h_bkg_pass = tmp.Clone("")
            h_bkg_pass.SetName(v._name+"_"+r+"_bkgpass")
        else:
            h_bkg_pass.Add(tmp)
        
    for f, s in zip(infile["Data"], insample["Data"]):
        histo_name = v._name+"_"+r
        tmp = copy.deepcopy(ROOT.TH1D(f.Get(histo_name)))
        tmp.SetTitle("")
        if h_data_pass==None:
            h_data_pass = tmp.Clone("")
            h_data_pass.SetName(v._name+"_"+r+"_datapass")
        else:
            h_data_pass.Add(tmp)

    # efficiencies histograms
    h_eff_data = h_data_pass.Clone("")
    h_eff_data.Divide(h_data_total)
    h_eff_bkg = h_bkg_pass.Clone("")
    h_eff_bkg.Divide(h_bkg_total)
    for i in range(1, h_eff_bkg.GetNbinsX() + 1):
        eff_bkg = h_eff_bkg.GetBinContent(i)
        eff_data = h_eff_data.GetBinContent(i)
        ntot_bkg = h_bkg_total.GetBinContent(i)
        ntot_data = h_data_total.GetBinContent(i)
        unc_bkg = math.sqrt(eff_bkg * (1 - eff_bkg) / ntot_bkg) if ntot_bkg > 0 else 0
        unc_data = math.sqrt(eff_data * (1 - eff_data) / ntot_data) if ntot_data > 0 else 0
        h_eff_bkg.SetBinError(i, unc_bkg)
        h_eff_data.SetBinError(i, unc_data)
        lowedge = h_eff_bkg.GetXaxis().GetBinLowEdge(i)
        upedge = h_eff_bkg.GetXaxis().GetBinUpEdge(i)
        print("MET bin [{}, {}]: bkg eff = {:.5f} +/- {:.5f}, data eff = {:.5f} +/- {:.5f}".format(lowedge, upedge, eff_bkg, unc_bkg, eff_data, unc_data))

    # plot
    outfileroot.cd()
    h_eff_data.Write()
    h_eff_bkg.Write()
    plot(h_eff_data, repostack, ROOT.kBlack, "TriggerEff_"+v._name+"_eff_data"+plotname, "Preliminary", 11, "13.6", str(lumi), "")
    plot(h_eff_bkg, repostack, ROOT.TColor.GetColor("#e42536"), "TriggerEff_"+v._name+"_eff_bkg"+plotname, "Preliminary", 11, "13.6", str(lumi), "")
    plot([h_eff_data, h_eff_bkg], repostack, ROOT.TColor.GetColor("#e42536"), "TriggerEff_"+v._name+"_eff"+plotname, "Preliminary", 11, "13.6", str(lumi), "")
    
    h_ratio = h_eff_bkg.Clone("")
    h_ratio.Divide(h_eff_data)
    h_ratio.SetName("SF1d")
    for i in range(1, h_ratio.GetNbinsX() + 1):
        eff_bkg = h_eff_bkg.GetBinContent(i)
        eff_data = h_eff_data.GetBinContent(i)
        unc_bkg = h_eff_bkg.GetBinError(i)
        unc_data = h_eff_data.GetBinError(i)
        sf = eff_data / eff_bkg if eff_data > 0 else 0
        unc_sf = math.sqrt((unc_data / eff_bkg)**2 + (unc_bkg/eff_bkg * sf)**2) if eff_bkg > 0 and eff_data > 0 else 0
        h_ratio.SetBinContent(i, sf)
        h_ratio.SetBinError(i, unc_sf)
        print("MET bin [{}, {}]: SF = {:.5f} +/- {:.5f}".format(h_ratio.GetXaxis().GetBinLowEdge(i), h_ratio.GetXaxis().GetBinUpEdge(i), sf, unc_sf))
    plot(h_ratio, repostack, ROOT.kBlack, "TriggerEff_"+v._name+"_SF"+plotname, "Preliminary", 11, "13.6", str(lumi), "", ytitle="SF")
    outfileroot.cd()
    h_ratio.Write()
    SF_MET_1D = h_ratio     # official SF vs MET, kept for the check of the inclusive curves of the jet-variable block below
# Plots 2D
h_bkg_total    = None
h_data_total   = None
h_bkg_pass     = None
h_data_pass    = None

for v in var2d:
    r = "orthogonalPreselR_Ntot"
    for i, (f,s) in enumerate(zip(infile2D["bkg"], insample["bkg"])):
        tmp = copy.deepcopy(ROOT.TH2D(f.Get(v._name+"_"+r)))
        if len(samples[s.label][s.label]["ntot"]):
            # tmp.Scale(s.sigma*(10**3)*lumi/np.sum(samples[s.label][s.label]["ntot"]))
            tmp.Scale(lumi)
        else:
            continue
        tmp.SetTitle("")
        if h_bkg_total==None:
            h_bkg_total = tmp.Clone("")
            h_bkg_total.SetName(v._name+"_"+r+"_bkgtotal")
        else:
            h_bkg_total.Add(tmp)
        
    for f, s in zip(infile2D["Data"], insample["Data"]):
        tmp = copy.deepcopy(f.Get(v._name+"_"+r))
        tmp.SetTitle("")
        if h_data_total==None:
            h_data_total = tmp.Clone("")
            h_data_total.SetName(v._name+"_"+r+"_datatotal")
        else:
            h_data_total.Add(tmp)

    r = "orthogonalPreselR_Npass"
    for i, (f,s) in enumerate(zip(infile2D["bkg"], insample["bkg"])):
        # print(v._name+"_"+r)
        tmp = copy.deepcopy(ROOT.TH2D(f.Get(v._name+"_"+r)))
        if len(samples[s.label][s.label]["ntot"]):
            # tmp.Scale(s.sigma*(10**3)*lumi/np.sum(samples[s.label][s.label]["ntot"]))
            tmp.Scale(lumi)
        else:
            continue
        tmp.SetTitle("")
        if h_bkg_pass==None:
            h_bkg_pass = tmp.Clone("")
            h_bkg_pass.SetName(v._name+"_"+r+"_bkgpass")
        else:
            h_bkg_pass.Add(tmp)
        
    for f, s in zip(infile2D["Data"], insample["Data"]):
        tmp = copy.deepcopy(f.Get(v._name+"_"+r))
        tmp.SetTitle("")
        if h_data_pass==None:
            h_data_pass = tmp.Clone("")
            h_data_pass.SetName(v._name+"_"+r+"_datapass")
        else:
            h_data_pass.Add(tmp)
    # efficiencies histograms
    h_eff_data = h_data_pass.Clone("")
    h_eff_data.Divide(h_data_total)
    h_eff_bkg = h_bkg_pass.Clone("")
    h_eff_bkg.Divide(h_bkg_total)
    for i in range(1, h_eff_bkg.GetNbinsX() + 1):
        for j in range(1, h_eff_bkg.GetNbinsY() + 1):
            eff_bkg = h_eff_bkg.GetBinContent(i, j)
            eff_data = h_eff_data.GetBinContent(i, j)
            ntot_bkg = h_bkg_total.GetBinContent(i, j)
            ntot_data = h_data_total.GetBinContent(i, j)
            unc_bkg = math.sqrt(eff_bkg * (1 - eff_bkg) / ntot_bkg) if ntot_bkg > 0 else 0
            unc_data = math.sqrt(eff_data * (1 - eff_data) / ntot_data) if ntot_data > 0 else 0
            h_eff_bkg.SetBinError(i, j, unc_bkg)
            h_eff_data.SetBinError(i, j, unc_data)
            lowedge_x = h_eff_bkg.GetXaxis().GetBinLowEdge(i)
            upedge_x = h_eff_bkg.GetXaxis().GetBinUpEdge(i)
            lowedge_y = h_eff_bkg.GetYaxis().GetBinLowEdge(j)
            upedge_y = h_eff_bkg.GetYaxis().GetBinUpEdge(j)
            print("MET bin [{}, {}], MHT bin [{}, {}]: bkg eff = {:.5f} +/- {:.5f}, data eff = {:.5f} +/- {:.5f}".format(lowedge_x, upedge_x, lowedge_y, upedge_y, eff_bkg, unc_bkg, eff_data, unc_data))

    # plot
    outfileroot.cd()
    h_eff_data.Write()
    h_eff_bkg.Write()
    plot2D(h_eff_bkg, repostack, var2d[0], canv_name="TriggerEff_2Dplot_eff_bkg"+plotname, extraTest="Preliminary", iPos=0, energy="13.6", lumi=str(lumi), addInfo="")
    plot2D(h_eff_data, repostack,var2d[0], canv_name="TriggerEff_2Dplot_eff_data"+plotname, extraTest="Preliminary", iPos=0, energy="13.6", lumi=str(lumi), addInfo="")
    # SF
    h_ratio = h_eff_data.Clone("")
    h_ratio.Divide(h_eff_bkg)
    h_ratio.SetName("SF2d")
    for i in range(1, h_ratio.GetNbinsX() + 1):
        for j in range(1, h_ratio.GetNbinsY() + 1):
            eff_bkg = h_eff_bkg.GetBinContent(i, j)
            eff_data = h_eff_data.GetBinContent(i, j)
            unc_bkg = h_eff_bkg.GetBinError(i, j)
            unc_data = h_eff_data.GetBinError(i, j)
            sf = eff_data / eff_bkg if eff_bkg > 0 else 0
            unc_sf = math.sqrt((unc_data / eff_bkg)**2 + (unc_bkg * eff_data)**2) if eff_bkg > 0 and eff_data > 0 else 0
            h_ratio.SetBinContent(i, j, sf)
            h_ratio.SetBinError(i, j, unc_sf)
            lowedge_x = h_ratio.GetXaxis().GetBinLowEdge(i)
            upedge_x = h_ratio.GetXaxis().GetBinUpEdge(i)
            lowedge_y = h_ratio.GetYaxis().GetBinLowEdge(j)
            upedge_y = h_ratio.GetYaxis().GetBinUpEdge(j)
            print("MET bin [{}, {}], MHT bin [{}, {}]: SF = {:.5f} +/- {:.5f}".format(lowedge_x, upedge_x, lowedge_y, upedge_y, sf, unc_sf))
    outfileroot.cd()
    h_ratio.Write()
    plot2D(h_ratio, repostack,var2d[0], canv_name="TriggerEff_2Dplot_SF"+plotname, extraTest="Preliminary", iPos=0, energy="13.6", lumi=str(lumi), addInfo="", ztitle="SF")


############### Trigger eff/SF vs MET in bins of the jet variables of the SR splitting (reviewer request, Nov 2026) ###############
# Input: <sample>_2D.root of TriggerSF/postSelector.py, TH2 with x = PuppiMET_T1_pt_nominal (same 12 bins as the SF) and y = jet variable.
# MC is already normalized to sigma/ntot in savehisto2d; here it is scaled to the lumi, as the 1D histograms above.
# The under/overflow of x and y is folded into the edge bins (merge_UnOvFlow2D): the last MET bin 500-1000 also contains MET > 1000,
# the 1D histogram above does not, so the inclusive curve can differ from the official SF only in that bin.
ROOT.TH1.AddDirectory(False)    # histograms created below (Clone, ProjectionX) are not owned by the open TFiles

jet_vars = [
    {"name"         : "PuppiMET_T1_pt_nominalVsnGoodJet",                   # name of the TH2 in the _2D.root files (+ "_" + region)
     "short"        : "nAK4",                                               # used in the output names
     "ytitle"       : "# AK4 jets",
     "slice_labels" : ["#leq 2 AK4", "3 AK4", "4 AK4", "5 AK4", "#geq 6 AK4"],
     "map_labels"   : ["#leq 2", "3", "4", "5", "#geq 6"],                  # y-axis labels of the 2D maps (None: no 2D map)
    },
    {"name"         : "PuppiMET_T1_pt_nominalVsnGoodFatJet",
     "short"        : "nAK8",
     "ytitle"       : "# AK8 jets",
     "slice_labels" : ["0 AK8", "1 AK8", "#geq 2 AK8"],
     "map_labels"   : ["0", "1", "#geq 2"],
    },
    {"name"         : "PuppiMET_T1_pt_nominalVsnForwardJet",
     "short"        : "nFJ",
     "ytitle"       : "# forward jets",
     "slice_labels" : ["0 FJ", "#geq 1 FJ"],
     "map_labels"   : ["0", "#geq 1"],
    },
    {"name"         : "PuppiMET_T1_pt_nominalVsLeadingJetPt_abseta",
     "short"        : "LeadingJetAbsEta",
     "ytitle"       : "Leading jet |#eta|",
     "slice_labels" : ["|#eta| < 0.8", "0.8 #leq |#eta| < 1.5", "1.5 #leq |#eta| < 2.4", "2.4 #leq |#eta| < 3.0", "|#eta| #geq 3.0"],
     "map_labels"   : ["0-0.8", "0.8-1.5", "1.5-2.4", "2.4-3.0", "#geq 3.0"],
    },
]
slice_colors    = ["#5790fc", "#f89c20", "#e42536", "#964a8b", "#9c9ca1"]   # one per y bin; the inclusive curve is black
slice_markers   = [21, 22, 23, 33, 34]

# _2D.root files, same order as insample
infile_jets     = {"Data": [], "bkg": []}
for key in ["Data", "bkg"]:
    for s in insample[key]:
        infile_jets[key].append(ROOT.TFile.Open(repohisto + s.label + "_2D.root"))


def sum_histos_2D(key, histo_name):
    # sum of the TH2 of all the components of Data (key="Data") or MC (key="bkg");
    # MC is scaled to the lumi, and components without ntot are skipped, as in the MET block above
    h_sum = None
    for f, s in zip(infile_jets[key], insample[key]):
        if key == "bkg" and len(samples[s.label][s.label]["ntot"]) == 0:
            continue
        h = f.Get(histo_name).Clone(histo_name + "_" + s.label)
        if key == "bkg":
            h.Scale(lumi)
        if h_sum is None:
            h_sum = h.Clone(histo_name + "_" + key + "sum")
        else:
            h_sum.Add(h)
    return h_sum


def eff_hist(h_pass, h_total, name):
    # efficiency pass/total in each bin (TH1 or TH2), binomial error sqrt(eff*(1-eff)/N_total) as in the MET block above
    h_eff = h_pass.Clone(name)
    h_eff.Divide(h_total)
    for b in range(h_eff.GetNcells()):
        if h_eff.IsBinUnderflow(b) or h_eff.IsBinOverflow(b):
            continue
        eff     = h_eff.GetBinContent(b)
        n_total = h_total.GetBinContent(b)
        unc     = math.sqrt(max(eff * (1 - eff), 0.) / n_total) if n_total > 0 else 0
        h_eff.SetBinError(b, unc)
    return h_eff


def sf_hist(h_eff_data, h_eff_mc, name):
    # SF = eff data / eff MC in each bin (TH1 or TH2), same error as the 1D SF above
    h_sf = h_eff_data.Clone(name)
    for b in range(h_sf.GetNcells()):
        if h_sf.IsBinUnderflow(b) or h_sf.IsBinOverflow(b):
            continue
        eff_data, unc_data  = h_eff_data.GetBinContent(b), h_eff_data.GetBinError(b)
        eff_mc, unc_mc      = h_eff_mc.GetBinContent(b), h_eff_mc.GetBinError(b)
        if eff_mc > 0 and eff_data > 0:
            sf      = eff_data / eff_mc
            unc_sf  = math.sqrt((unc_data / eff_mc)**2 + (unc_mc / eff_mc * sf)**2)
        else:
            sf, unc_sf = 0, 0
        h_sf.SetBinContent(b, sf)
        h_sf.SetBinError(b, unc_sf)
    return h_sf


def shifted_graph(h, shift):
    # TGraphErrors of h with the points moved by shift*(bin width) along x, so that the overlaid curves do not hide each other;
    # x error = half bin width, empty bins (content 0) are skipped
    g = ROOT.TGraphErrors()
    for i in range(1, h.GetNbinsX() + 1):
        if h.GetBinContent(i) <= 0:
            continue
        width   = h.GetXaxis().GetBinWidth(i)
        x       = h.GetXaxis().GetBinCenter(i) + shift * width
        n       = g.GetN()
        g.SetPoint(n, x, h.GetBinContent(i))
        g.SetPointError(n, width / 2, h.GetBinError(i))
    return g


def plot_overlay(h_inclusive, h_slices, labels, canv_name, ytitle, y_min, y_max, legend_title):
    # inclusive curve (black) + one curve per bin of the jet variable, cmsstyle as plot() above
    CMS.SetExtraText("Preliminary")
    CMS.SetLumi(str(lumi))
    CMS.SetEnergy("13.6")
    CMS.ResetAdditionalInfo()
    x_min   = h_inclusive.GetXaxis().GetXmin()
    x_max   = h_inclusive.GetXaxis().GetXmax()
    canv    = cms_canvas_1D(canv_name, x_min, x_max, y_min, y_max, h_inclusive.GetXaxis().GetTitle() or "p_{T}^{miss}(Puppi) [GeV]", ytitle)
    leg     = CMS.cmsLeg(0.42, 0.68, 0.93, 0.89, textSize=0.035)
    leg.SetNColumns(2)
    leg.SetHeader(legend_title)

    if ytitle == "SF":
        line = ROOT.TLine(x_min, 1., x_max, 1.)
        line.SetLineStyle(2)
        line.SetLineColor(ROOT.kGray + 1)
        line.Draw("same")

    n_curves    = len(h_slices) + 1
    shifts      = [0.08 * (k - (n_curves - 1) / 2.) for k in range(n_curves)]   # symmetric around the bin center
    graphs      = []
    g_incl      = shifted_graph(h_inclusive, shifts[0])
    CMS.cmsDraw(g_incl, "P", marker=20, msize=1.0, mcolor=ROOT.kBlack, lcolor=ROOT.kBlack)
    leg.AddEntry(g_incl, "inclusive", "lp")
    graphs.append(g_incl)
    for k, (h, label) in enumerate(zip(h_slices, labels)):
        color   = ROOT.TColor.GetColor(slice_colors[k])
        g       = shifted_graph(h, shifts[k + 1])
        CMS.cmsDraw(g, "P", marker=slice_markers[k], msize=1.0, mcolor=color, lcolor=color)
        leg.AddEntry(g, label, "lp")
        graphs.append(g)
    leg.Draw("same")
    save_pdf(canv, repostack + "/pdf/1D/" + canv_name + ".pdf")


def plot_map(h, canv_name, ytitle, ylabels, ztitle, z_min, z_max):
    # 2D map with all the bins of the same size on the plot (user convention), the x-axis labels show the real MET bin edges;
    # each bin shows value +- error
    nx, ny  = h.GetNbinsX(), h.GetNbinsY()
    h_plot  = ROOT.TH2D(h.GetName() + "_plot", "", nx, 0, nx, ny, 0, ny)
    for ix in range(1, nx + 1):
        for iy in range(1, ny + 1):
            h_plot.SetBinContent(ix, iy, h.GetBinContent(ix, iy))
            h_plot.SetBinError(ix, iy, h.GetBinError(ix, iy))
    for ix in range(1, nx + 1):
        h_plot.GetXaxis().SetBinLabel(ix, f"{h.GetXaxis().GetBinLowEdge(ix):g}-{h.GetXaxis().GetBinUpEdge(ix):g}")
    for iy in range(1, ny + 1):
        h_plot.GetYaxis().SetBinLabel(iy, ylabels[iy - 1])
    h_plot.SetTitle(f";p_{{T}}^{{miss}}(Puppi) [GeV];{ytitle};{ztitle}")
    h_plot.SetMinimum(z_min)
    h_plot.SetMaximum(z_max)
    for axis in [h_plot.GetXaxis(), h_plot.GetYaxis(), h_plot.GetZaxis()]:
        axis.SetTitleFont(42)
        axis.SetLabelFont(42)
        axis.SetTitleSize(0.045)
    h_plot.GetXaxis().SetLabelSize(0.045)
    h_plot.GetXaxis().LabelsOption("h")         # horizontal labels (after the cmsCanvas of the plots above they come out tilted)
    h_plot.GetXaxis().SetTitleOffset(1.5)
    h_plot.GetYaxis().SetLabelSize(0.055)
    h_plot.GetYaxis().SetTitleOffset(1.45)        # room for the longest labels (|eta| bins, e.g. 2.4-3.0)
    h_plot.GetZaxis().SetLabelSize(0.04)
    h_plot.GetZaxis().SetTitleOffset(1.0)
    h_plot.SetMarkerSize(1.15)                  # size of the text in the bins
    ROOT.gStyle.SetPaintTextFormat("4.3f")
    ROOT.gStyle.SetPalette(ROOT.kViridis)       # as CMS.SetCMSPalette(), which needs a cmsCanvas drawn before

    canv    = ROOT.TCanvas(canv_name, "", 1400, 800)
    canv.SetLeftMargin(0.14)
    canv.SetRightMargin(0.13)
    canv.SetBottomMargin(0.16)
    canv.SetTopMargin(0.07)
    h_plot.Draw("COLZ TEXT E")
    latex   = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.SetTextSize(0.05)
    latex.SetTextAlign(11)
    latex.DrawLatex(0.14, 0.945, "#bf{CMS} #it{Preliminary}")
    latex.SetTextAlign(31)
    latex.DrawLatex(0.87, 0.945, f"{lumi} fb^{{-1}} (13.6 TeV)")
    save_pdf(canv, repostack + "/pdf/2D/" + canv_name + ".pdf")


def print_table(title, h_inclusive, h_slices, labels):
    # one row per bin of the jet variable, one column per MET bin: value +- error
    print(f"\n{title}")
    met_bins = [f"{h_inclusive.GetXaxis().GetBinLowEdge(i):g}-{h_inclusive.GetXaxis().GetBinUpEdge(i):g}" for i in range(1, h_inclusive.GetNbinsX() + 1)]
    print(f"{'':>24s} " + " ".join(f"{b:>15s}" for b in met_bins))
    for label, h in [("inclusive", h_inclusive)] + list(zip(labels, h_slices)):
        values = [f"{h.GetBinContent(i):.3f}+-{h.GetBinError(i):.3f}" for i in range(1, h.GetNbinsX() + 1)]
        print(f"{label.replace('#', ''):>24s} " + " ".join(f"{v:>15s}" for v in values))


for jv in jet_vars:
    name    = jv["name"]
    short   = jv["short"]
    print(f"\n################ Trigger efficiency/SF vs MET in bins of {short} ################")
    # summed TH2: Data and MC, total and passing the MET trigger
    h_data_tot  = sum_histos_2D("Data", name + "_orthogonalPreselR_Ntot")
    h_data_pass = sum_histos_2D("Data", name + "_orthogonalPreselR_Npass")
    h_mc_tot    = sum_histos_2D("bkg",  name + "_orthogonalPreselR_Ntot")
    h_mc_pass   = sum_histos_2D("bkg",  name + "_orthogonalPreselR_Npass")
    ny          = h_data_tot.GetNbinsY()

    # 2D: efficiencies and SF in each (MET, jet variable) bin
    h2_eff_data = eff_hist(h_data_pass, h_data_tot, f"TriggerEff_2D_METvs{short}_effData")
    h2_eff_mc   = eff_hist(h_mc_pass,   h_mc_tot,   f"TriggerEff_2D_METvs{short}_effMC")
    h2_sf       = sf_hist(h2_eff_data, h2_eff_mc,   f"TriggerEff_2D_METvs{short}_SF")

    # 1D: projections on MET, inclusive (all the y bins) and one per y bin
    def projections(h2, tag):
        inclusive   = h2.ProjectionX(f"{h2.GetName()}_{tag}_incl", 1, ny)
        slices      = [h2.ProjectionX(f"{h2.GetName()}_{tag}_bin{j}", j, j) for j in range(1, ny + 1)]
        return inclusive, slices
    data_tot_incl,  data_tot_slices     = projections(h_data_tot,  "p")
    data_pass_incl, data_pass_slices    = projections(h_data_pass, "p")
    mc_tot_incl,    mc_tot_slices       = projections(h_mc_tot,    "p")
    mc_pass_incl,   mc_pass_slices      = projections(h_mc_pass,   "p")

    eff_data_incl   = eff_hist(data_pass_incl, data_tot_incl, f"TriggerEff_{short}_inclusive_effData")
    eff_mc_incl     = eff_hist(mc_pass_incl,   mc_tot_incl,   f"TriggerEff_{short}_inclusive_effMC")
    sf_incl         = sf_hist(eff_data_incl, eff_mc_incl,     f"TriggerEff_{short}_inclusive_SF")
    eff_data_slices = [eff_hist(data_pass_slices[j], data_tot_slices[j], f"TriggerEff_{short}_bin{j+1}_effData") for j in range(ny)]
    eff_mc_slices   = [eff_hist(mc_pass_slices[j],   mc_tot_slices[j],   f"TriggerEff_{short}_bin{j+1}_effMC")   for j in range(ny)]
    sf_slices       = [sf_hist(eff_data_slices[j], eff_mc_slices[j],     f"TriggerEff_{short}_bin{j+1}_SF")      for j in range(ny)]

    # check: the inclusive SF must be the official SF vs MET of the block above (all bins except the last one, see the comment on top)
    for i in range(1, sf_incl.GetNbinsX() + 1):
        sf_official = SF_MET_1D.GetBinContent(i)
        diff        = abs(sf_incl.GetBinContent(i) - sf_official) / sf_official if sf_official > 0 else 0
        if diff > 1e-6:
            print(f"CHECK inclusive SF vs official SF, MET bin {i}: {sf_incl.GetBinContent(i):.5f} vs {sf_official:.5f} (rel diff {diff:.2e})")

    print_table(f"SF vs MET, bins of {short}",       sf_incl,       sf_slices,       jv["slice_labels"])
    print_table(f"eff data vs MET, bins of {short}", eff_data_incl, eff_data_slices, jv["slice_labels"])
    print_table(f"eff MC vs MET, bins of {short}",   eff_mc_incl,   eff_mc_slices,   jv["slice_labels"])

    # plots: curves vs MET per bin of the jet variable
    # SF y range from the points with error < 0.05 (a few low-stat bins, e.g. 0 AK8 at MET 500-1000, would squash the plot; they end up
    # out of the frame); the points stay in the lower ~60% of the frame, the legend is above them
    sf_points   = [(h.GetBinContent(i), h.GetBinError(i)) for h in [sf_incl] + sf_slices for i in range(1, h.GetNbinsX() + 1)
                   if h.GetBinContent(i) > 0 and h.GetBinError(i) < 0.05]
    sf_low      = min(v - e for v, e in sf_points) - 0.05
    sf_high     = max(v + e for v, e in sf_points)
    sf_top      = sf_low + (sf_high - sf_low) / 0.6
    plot_overlay(sf_incl,       sf_slices,       jv["slice_labels"], f"TriggerEff_{short}_slices_SF",      "SF",                 sf_low, sf_top, jv["ytitle"])
    plot_overlay(eff_data_incl, eff_data_slices, jv["slice_labels"], f"TriggerEff_{short}_slices_effData", "Efficiency (data)",  0., 1.65, jv["ytitle"])
    plot_overlay(eff_mc_incl,   eff_mc_slices,   jv["slice_labels"], f"TriggerEff_{short}_slices_effMC",   "Efficiency (MC)",    0., 1.65, jv["ytitle"])

    # plots: 2D maps
    if jv["map_labels"] is not None:
        # z range from the bins with error < 0.05, as the SF curves above (the low-stat bins get the color of the edge of the scale)
        sf_map_values = [h2_sf.GetBinContent(i, j) for i in range(1, h2_sf.GetNbinsX() + 1) for j in range(1, ny + 1)
                         if h2_sf.GetBinContent(i, j) > 0 and h2_sf.GetBinError(i, j) < 0.05]
        plot_map(h2_eff_data, f"TriggerEff_2D_METvs{short}_effData", jv["ytitle"], jv["map_labels"], "Efficiency (data)", 0., 1.)
        plot_map(h2_eff_mc,   f"TriggerEff_2D_METvs{short}_effMC",   jv["ytitle"], jv["map_labels"], "Efficiency (MC)",   0., 1.)
        plot_map(h2_sf,       f"TriggerEff_2D_METvs{short}_SF",      jv["ytitle"], jv["map_labels"], "SF",                min(sf_map_values), max(sf_map_values))

    outfileroot.cd()
    for h in [h2_eff_data, h2_eff_mc, h2_sf, eff_data_incl, eff_mc_incl, sf_incl] + eff_data_slices + eff_mc_slices + sf_slices:
        h.Write()

# Close ROOT files before terminating. With the LCG 107 PyROOT build,
# leaving their destruction to Python finalization can crash in CPyCppyy.
outfileroot.Close()
for file_list in list(infile.values()) + list(infile2D.values()) + list(infile_jets.values()):
    for root_file in file_list:
        if root_file:
            root_file.Close()

sys.stdout.flush()
sys.stderr.flush()
ROOT.gSystem.Exit(0)