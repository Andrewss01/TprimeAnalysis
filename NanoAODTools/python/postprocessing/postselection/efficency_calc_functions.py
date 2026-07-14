import ROOT 

def count_num_events(file_path, variable, region, syst ='nominal'):
    print(file_path)
    rfile = ROOT.TFile.Open(file_path, 'READ')
    key = variable + '_' + region +"_" + syst
    histo  = rfile.Get(key)
    # num_event = histo.Integral()
    # print('num _event is: ', histo.GetEntries())
    num_event = histo.GetEntries()
    return num_event

# path = "/eos/user/a/apuglia/Tprime/regions_histo_trota/plots/TprimeToTZ_700_2022.root"
# rfile = ROOT.TFile.Open(path,"READ")
# keys = []
# for key in rfile.GetListOfKeys():
#     keys.append(key.GetName())
# histo.Get("PuppiMET_pt_SR_nominal")
# print(len(keys))

regions = ["btagSFcheck","SR","SR0fjets","SRatleast1fjets","SRTopRes","SRTopRes0fjets","SRTopResatleast1fjets","SRTopMix","SRTopMix0fjets","SRTopMixatleast1fjets",
            "SRTopMer","SRTopMer0fjets","SRTopMeratleast1fjets","SRTop","SRTop0fjets","SRTopatleast1fjets","SRTopLoose","SRTop0fjetsLoose","SRTopatleast1fjetsLoose",
            "SRTopResLoose","SRTop0fjetsResLoose","SRTopatleast1fjetsResLoose","SRTopMixLoose","SRTop0fjetsMixLoose","SRTopatleast1fjetsMixLoose","SRTopMerLoose",
            "SRTop0fjetsMerLoose","SRTopatleast1fjetsMerLoose","AH","SL" ,"AH1lWR","AH0lZR"]

variables = ["PuppiMET_pt", "PuppiMET_phi", "PuppiMET_T1_pt_nominal", "PuppiMET_T1_phi_nominal", 
            "LeadingJetPt_pt", "LeadingFatJetPt_pt", "LeadingFatJetPt_msoftdrop", "nTightTopMixed", 
            "nTightTopResolved", "nJet", "nJetBtagMedium", "nJetBtagLoose", "nFatJet", "MinDelta_phi",
            "HT_eventHT", "MHT", "PV_npvsGood", "TopMixed_TopScore_nominal", "TopResolved_TopScore_nominal", 
            "EventTopCategory","Top_mass", "Top_pt", "Top_score", "MT_T", "FatJet_particleNetWithMass_TvsQCD", 
            "FatJet_msoftdrop_nominal"]

variations = ["nominal", "pu_up", "pu_down", "jer_up", "jer_down","jesTotal_up","jesTotal_down", "pfd_total_up","pdf_total_down", 
            "QCDScale_up", "QCDScale_down", "ISR_up", "ISR_down","FSR_up","FSR_down"]

# sum=0
# for var in variables: 
#     for reg in regions:
#         for syst in variations:
#             sum +=1

# print(sum)