import ROOT 
import os
import optparse
from efficency_calc_functions import * 
import array

usage                   = 'python3 efficiency_plot.py'
parser                  = optparse.OptionParser(usage)
# parser.add_option('-f', '--folder'     , dest='folder'     , type=list, default='regions_histos/'            , help='one or more folder with the histos' )
parser.add_option('-r', '--region'     , dest='region'     , type=str , default='SRTopRes'                   , help='region to calculate the efficiency' )
parser.add_option('-v', '--variable'   , dest='variable'   , type=str , default='PuppiMET_pt'                , help='variable to use'                    )
parser.add_option('-d', '--denominator', dest='denominator', type=str , default='SR'                         , help='region to do the efficiency'        )
parser.add_option('-s', '--saving'     , dest='saving'     , type=str , default='results/'                      , help='folder where to save plots'         )
# parser.add_option('-s', '--sample'     , dest='sample'     , type=str, default='ZJets'                      ,)


(opt, args)             = parser.parse_args()

# folder_name = opt.folder
folders = ["regions_histos/trota2d_histos_tight_v1/plots/", "regions_histos/trota_histos_tight_v1/plots/"]
region      = opt.region
variable    = opt.variable
denominator = opt.denominator
plot_folder = opt.saving


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


plots_folder  = os.environ.get('PWD') + "/" + plot_folder

mtprime_values = [700,800,900,1000,1200,1300,1400,1500,1600,1700]

f = open('num_events_'+region+'_vs_'+denominator+'.txt',"w")
eff_values = {'trota2d': [], 'trota':[]}

# for file_root in os.listdir(histos_folder):
for folder_ in folders:
    print('folder is: ', folder_)
    folder = os.environ.get('PWD')+"/"+folder_
    f.write(f"folder: {folder_}\n")
    effs = []
    for mt_ in mtprime_values:
        total_events, total_tight = 0,0
        f.write(f"m_tprime: {mt_} ")
        file_name = "TprimeToTZ_"+str(mt_)+"_2022.root"
        file_path = folder+file_name

        num_total_tprime = count_num_events(file_path, variable, denominator)
        num_tight_tprime = count_num_events(file_path, variable, region)
        # print('mt is: ', mt_)
        # print('nm total tprime: ', num_total_tprime)
        f.write(f"events is {region} {num_tight_tprime} ")
        f.write(f"events in {denominator} {num_total_tprime} ")
        eff = num_tight_tprime/num_total_tprime
        # /num_total_tprime 
        f.write(f"efficiency: {eff}\n")
        # print('eff is: ', eff)

        effs.append(eff)
    
    if 'trota2d' in folder_:
        # print(folder_)
        eff_values['trota2d'] = effs
    else: 
        eff_values['trota'] = effs
        
trota2d_values = eff_values['trota2d']
trota_values   = eff_values['trota']
f.close()

print(len(mtprime_values))
print(len(trota_values))

graph_trota   = ROOT.TGraph(len(mtprime_values), array.array('f',mtprime_values), array.array('f',trota_values  ))
graph_trota2d = ROOT.TGraph(len(mtprime_values), array.array('f',mtprime_values), array.array('f',trota2d_values))

graph_trota2d.GetXaxis().SetTitle('mtprime')
graph_trota2d.GetYaxis().SetTitle('efficiency')
# graph_trota2d.SetLineColor(ROOT.kBlue)
graph_trota2d.SetMarkerColor(ROOT.kBlue)
graph_trota2d.SetMarkerStyle(20)


# graph_trota2d.SetLineColor(ROOT.Green)
graph_trota.SetMarkerColor(ROOT.kGreen)
graph_trota.SetMarkerStyle(21)

c = ROOT.TCanvas()
# A = assi, P = punti, L = linee
graph_trota.Draw("AP")
graph_trota2d.Draw("SAMEP")  


leg = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
leg.AddEntry(graph_trota, "TROTA", "lp")
leg.AddEntry(graph_trota2d, "TROTA 2D ", "lp")



leg.SetBorderSize(0)     
leg.SetFillStyle(0)      
leg.SetTextSize(0.03)    
leg.SetHeader("Legend")  
leg.Draw()

c.Draw()
c.SaveAs("efficiency_"+region+"_vs_"+denominator+".png")