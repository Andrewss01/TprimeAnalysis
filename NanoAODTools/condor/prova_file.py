import ROOT

file_path = '/store/user/apuglia/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/TT_semilep_2022_v1/251103_093221/0000/nano_mcRun3_264.root'

# file = ROOT.TFile.Open('root://cms-xrd-global.cern.ch/'+ file_path, 'READ')
file = ROOT.TFile('tmp/ZJetsToNuNu_2jets_PT100to200_1J_2022/file0/tree.root', 'READ')
file.ls()


tree = file.Get('Events')
tree.Print('TopMixed*')