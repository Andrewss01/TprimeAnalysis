#!/usr/bin/env python3
import ROOT 

file_path = "/eos/user/a/apuglia/TROTA/Study_pt_distribution/histos/pt_topmixed.root"

rfile = ROOT.TFile.Open(file_path, 'READ')



histo_sig = ROOT.TH1F("pt_sig_samples", "pT distribution Signal Samples", 200,0,1000)
histo_qcd = ROOT.TH1F("pt_qcd_samples", "pT distribution QCD/ZJ Samples", 200,0,1000)
histo_ft  = ROOT.TH1F("pt_ft_samples" , "pT distribution False Top Samples" , 200,0,1000)
# c_sig = ROOT.TCanvas('compare_sig', 'compare_sig')
# c_qcd = ROOT.TCanvas('compare_bkg', 'compare_bkg')
# c_ft  = ROOT.TCanvas('comprare_ft', 'compare_ft' )
# c_sig_qcd = ROOT.TCanvas('compare_sig_bkg', 'compare_sig_bkg')
# c_sig_ft  = ROOT.TCanvas('compare_sig_ft' , 'compare_sig_ft')
for i in rfile.GetListOfKeys():
    key = i.GetName()
    print(key)
    if "ZJetsToNuNu_2022" not in key: 
        if "true_tops" in key: 
            h1 = rfile.Get(key)
            histo_sig.Add(h1)
            
            # c_sig.cd()
            # h1.Draw('SAME')
        elif "false_tops" in key and ("ZJ" in key): 
            h2 = rfile.Get(key)
            histo_qcd.Add(h2)
            # c_bkg.cd()
            # h2.Draw('SAME')
    
        elif "false_tops" in key and  ("QCD" in key):
            h2 = rfile.Get(key)
            histo_qcd.Add(h2)
        
        else:
            h3 = rfile.Get(key)
            histo_ft.Add(h3)
        

 

# rfile.Close()

out_file = "/eos/user/a/apuglia/TROTA/Study_pt_distribution/pt_topmixed_pt600.root"
outfile = ROOT.TFile.Open(out_file, 'RECREATE')
histo_sig.Write()
histo_qcd.Write()
histo_ft.Write()

histo_ft.GetXaxis().SetTitle("pT [GeV]")
histo_ft.GetXaxis().SetTitle("Events")
histo_qcd.GetXaxis().SetTitle("pT [GeV]")
histo_qcd.GetXaxis().SetTitle("Events")

c1 = ROOT.TCanvas("sig_vs_qcd_pt", "pT Signal vs QCD Samples")
histo_qcd.SetLineColor(ROOT.kBlue)
histo_sig.SetLineColor(ROOT.kGreen)
histo_ft.SetLineColor(ROOT.kRed)
histo_qcd.Draw()
histo_sig.Draw('SAME')
c1.Write()

# c_sig.Write()
# c_bkg.Write()

c2 = ROOT.TCanvas("sig_vs_ft_pt", "pT Signal vs False Top Samples")

histo_ft.Draw()
histo_sig.Draw('SAME')
c2.Write()
outfile.Close()

# histo_1 = rfile.Get("pT_TprimeToTZ_700_2022_true_tops")
# histo_2 = rfile.Get("pT_TprimeToTZ_800_2022_true_tops")
# histo_sig.Add(histo_2)
# histo_sig.Write()
# print(h3)2