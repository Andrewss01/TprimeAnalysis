import ROOT 
import os
import optparse
from efficency_calc_functions import * 
import array

usage                   = 'python3 efficiency_plot.py'
parser                  = optparse.OptionParser(usage)
# parser.add_option('-f', '--folder'     , dest='folder'     , type=list, default='regions_histos/'            , help='one or more folder with the histos' )
parser.add_option('-r', '--region'     , dest='region'     , type=str , default='SRTopMix'                   , help='region to calculate the efficiency' )
parser.add_option('-v', '--variable'   , dest='variable'   , type=str , default='PuppiMET_pt'                , help='variable to use'                    )
parser.add_option('-d', '--denominator', dest='denominator', type=str , default='SR'                         , help='region to do the efficiency'        )
parser.add_option('-s', '--saving'     , dest='saving'     , type=str , default='efficiency_studies/'                      , help='folder where to save plots'         )
# parser.add_option('-s', '--sample'     , dest='sample'     , type=str, default='ZJets'                      ,)


(opt, args)             = parser.parse_args()

# folder_name = opt.folder
folders = ["regions_histo_trota2d/plots/", "regions_histo_trota/plots/"]
region      = opt.region
variable    = opt.variable
denominator = opt.denominator
save_folder = opt.saving



if region not in regions: 
    print('Insert a correct value for the region')
    exit()
if variable not in variables: 
    print('Inert a valid value for the variable')
    exit()
if denominator not in regions: 
    print('Insert a valid value for the region (denominator)')
    exit()


output_folder  = "/eos/user/a/apuglia/Tprime/" + save_folder

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

mtprime_values = [700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800]
zjets_values = ["600","400to600","200to400","100to200","40to100"]
f = open(f'{output_folder}num_events_{variable}_{region}_vs_{denominator}.txt',"w")
eff_values = {'trota2d': [], 'trota':[]}

# for file_root in os.listdir(histos_folder):
for folder_ in folders:
    
    folder = "/eos/user/a/apuglia/Tprime/"+folder_
    f.write(f"folder: {folder_}\n")
    effs = []
    for mt_ in mtprime_values:
        total_events, total_tight = 0,0
        f.write(f"m_tprime: {mt_} ")
        file_name = "TprimeToTZ_"+str(mt_)+"_2022.root"
        file_path = folder+file_name

        num_total_tprime = count_num_events(file_path, variable, denominator)
        num_tight_tprime = count_num_events(file_path, variable, region)
       
        f.write(f"events is {region} {num_tight_tprime} ")
        f.write(f"events in {denominator} {num_total_tprime} ")
        eff = num_tight_tprime/num_total_tprime
    
        f.write(f"efficiency: {eff}\n")


        effs.append(eff)
    
    if 'trota2d' in folder_:
        
        eff_values['trota2d'] = effs
    else: 
        eff_values['trota'] = effs
    num_total_zjets, num_selected_zjets = 0,0
    for zj in zjets_values:
        for num_jet in ["1J","2J"]:
            file_name = "ZJetsToNuNu_2jets_PT"+str(zj)+"_"+str(num_jet)+"_2022.root"
            file_path = folder+ file_name
            total_zjets = count_num_events(file_path, variable,denominator)
            selected_zjets = count_num_events(file_path,variable, region)
            num_total_zjets += total_zjets
            num_selected_zjets += selected_zjets
    
    f.write(f"ZJETS events in {region} {num_selected_zjets} ZJETS events in {denominator} {num_total_zjets} efficiency {num_selected_zjets/num_total_zjets}\n")
        
trota2d_values = eff_values['trota2d']
trota_values   = eff_values['trota']
f.close()

print(len(mtprime_values))
print(len(trota_values))
print(len(trota2d_values))

graph_trota   = ROOT.TGraph(len(mtprime_values), array.array('f',mtprime_values), array.array('f',trota_values  ))
graph_trota2d = ROOT.TGraph(len(mtprime_values), array.array('f',mtprime_values), array.array('f',trota2d_values))

graph_trota2d.GetXaxis().SetTitle('mtprime')
graph_trota2d.GetYaxis().SetTitle('efficiency')

graph_trota2d.SetMarkerColor(ROOT.kBlue)
graph_trota2d.SetMarkerStyle(20)


graph_trota.SetMarkerColor(ROOT.kGreen)
graph_trota.SetMarkerStyle(21)

c = ROOT.TCanvas()

graph_trota2d.Draw("AP")  
graph_trota.Draw("SAMEP")



leg = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
leg.AddEntry(graph_trota, "TROTA", "lp")
leg.AddEntry(graph_trota2d, "TROTA 2D ", "lp")



leg.SetBorderSize(0)     
leg.SetFillStyle(0)      
leg.SetTextSize(0.03)    
leg.SetHeader("Legend")  
leg.Draw()

c.Draw()
c.SaveAs(f"{output_folder}efficiency_{variable}_{region}_vs_{denominator}.png")