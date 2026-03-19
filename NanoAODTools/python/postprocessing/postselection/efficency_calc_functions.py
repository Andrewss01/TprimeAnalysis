import ROOT 

def count_num_events(file_path, variable, region):
    rfile = ROOT.TFile.Open(file_path, 'READ')
    key = variable + '_' + region
    histo  = rfile.Get(key)
    # num_event = histo.Integral()
    # print('num _event is: ', histo.GetEntries())
    num_event = histo.GetEntries()
    return num_event

