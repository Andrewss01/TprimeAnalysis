import ROOT 
import os
import optparse

usage                   = 'python3 efficiency_cal.py'
parser                  = optparse.OptionParser(usage)
parser.add_option('-f', '--folder'     , dest='folder'     , type=str, default='regions_histos/trota_histos_tight_v1/plots', help='folder with the histos'             )
parser.add_option('-r', '--region'     , dest='region'     , type=str, default='SRTopMix'                     , help='region to calculate the efficiency' )
parser.add_option('-v', '--variable'   , dest='variable'   , type=str, default='TopMixed_TopScore_nominal'                , help='variable to use'                    )
parser.add_option('-d', '--denominator', dest='denominator', type=str, default='SR'                         , help='region to do the efficiency'        )
# parser.add_option('-s', '--sample'     , dest='sample'     , type=str, default='ZJets'                      ,)


(opt, args)             = parser.parse_args()

folder_name = opt.folder
region      = opt.region
variable    = opt.variable
denominator = opt.denominator


regions = ["btagSFcheck","SR","SR0fjets","SRatleast1fjets","SRTopRes","SRTopRes0fjets","SRTopResatleast1fjets","SRTopMix","SRTopMix0fjets","SRTopMixatleast1fjets",
            "SRTopMer","SRTopMer0fjets","SRTopMeratleast1fjets","SRTop","SRTop0fjets","SRTopatleast1fjets","SRTopLoose","SRTop0fjetsLoose","SRTopatleast1fjetsLoose",
            "SRTopResLoose","SRTop0fjetsResLoose","SRTopatleast1fjetsResLoose","SRTopMixLoose","SRTop0fjetsMixLoose","SRTopatleast1fjetsMixLoose","SRTopMerLoose",
            "SRTop0fjetsMerLoose","SRTopatleast1fjetsMerLoose","AH","AHResLoose","AHMixLoose","AHMerLoose","AHLoose","SL","SLResLoose","SLMixLoose","SLMerLoose",
            "SLLoose","AH1lWR","AH1lWRResLoose","AH1lWRMixLoose","AH1lWRMerLoose","AH1lWRLoose","AH0lZR","AH0lZRResLoose","AH0lZRMixLoose","AH0lZRMerLoose","AH0lZRLoose"]

variables = [ "PuppiMET_pt", "PuppiMET_phi", "PuppiMET_T1_pt_nominal", "PuppiMET_T1_phi_nominal", "LeadingJetPt_pt", "LeadingFatJetPt_pt", "LeadingFatJetPt_msoftdrop",
              "nTopMixed", "nTopResolved", "nJet", "nJetBtagMedium", "nJetBtagLoose", "nFatJet", "MinDelta_phi", "HT_eventHT", "MHT", "PV_npvsGood", "TopMixed_TopScore_nominal", 
              "TopResolved_TopScore_nominal", "EventTopCategory", "Top_mass", "Top_pt", "Top_score", "MT_T", "FatJet_particleNetWithMass_TvsQCD", "FatJet_msoftdrop_nominal"]

if region not in regions: 
    print('Insert a correct value for the region')
    exit()
if variable not in variables: 
    print('Inert a valid value for the variable')
    exit()
if denominator not in regions: 
    print('Insert a valid value for the region (denominator)')
    exit()

histos_folder = os.environ.get('PWD') + "/" + folder_name

num_total_zjets, num_selected_zjets = 0,0
num_total_tprime, num_selected_tprime = 0,0
for file_root in os.listdir(histos_folder):
    if file_root.endswith('.root'):
        # print(file_root)
        if "ZJets" in file_root:
            # print(f"File is: {file_root}") 
            rfile = ROOT.TFile.Open(histos_folder+"/"+file_root, 'READ')
            
            key_total    = variable+'_'+denominator
            key_selected = variable+'_'+region 

            histo_total    = rfile.Get(key_total)
            histo_selected = rfile.Get(key_selected)

            events_sr  = histo_total.GetEntries()
            events_reg = histo_selected.GetEntries()

            # print(f"events {denominator}: {events_sr}")
            # print(f"events {region}: {events_reg}")
            num_total_zjets += events_sr
            num_selected_zjets += events_reg
        
        if "TprimeToTZ_800" in file_root: 
            # print(f"File is: {file_root}")
            rfile = ROOT.TFile.Open(histos_folder+"/"+file_root,'READ')

            key_total    = variable+'_'+denominator
            key_selected = variable+'_'+region

            histo_total    = rfile.Get(key_total)
            histo_selected = rfile.Get(key_selected)

            events_sr  = histo_total.GetEntries()
            events_reg = histo_selected.GetEntries()

            # print(f"events {denominator}: {events_sr}")
            # print(f"events {region}: {events_reg}")

            num_total_tprime    += events_sr
            num_selected_tprime += events_reg

if num_total_zjets != 0:
    eff_zjets  = num_selected_zjets/num_total_zjets
    print(f"total number of events in SR region for ZJets: {num_total_zjets}")
    print(f"total number of events in the {region} region for ZJets: {num_selected_zjets}")
    print(f"efficiency for ZJets: {eff_zjets}")

if num_total_tprime != 0:
    eff_tprime = num_selected_tprime/num_total_tprime
    print(f"total number of events in the {denominator} region for Tprime: {num_total_tprime}")
    print(f"total number of events in the {region} region for Tprime: {num_selected_tprime}")
    print(f"efficiency for Tprime: {eff_tprime}")



            
            
            
