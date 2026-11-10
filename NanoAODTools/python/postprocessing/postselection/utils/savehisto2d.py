import ROOT
from PhysicsTools.NanoAODTools.postprocessing.postselection.utils.merge_UnOvFlow import merge_UnOvFlow2D

def savehisto2d(d, dict_h, regions_def, var2d, outfolder, ntot_events):
    # dict_h[d.label][s.label][reg][v._name]: histograms booked by bookhisto2D
    # writes one file per component: outfolder+<sample>_2D.root
    # under/overflow folded into the edge bins (merge_UnOvFlow2D);
    # MC histograms are normalized to sigma*10**3/ntot_events[d.label][s.label], as in savehisto
    isMC = True
    if "Data" in d.label: isMC = False
    if hasattr(d, "components"):
        s_list = d.components
    else:
        s_list = [d]

    for s in s_list:
        outfile = ROOT.TFile.Open(outfolder+s.label+'_2D.root', "RECREATE")
        for reg in regions_def.keys():
            for v in var2d:
                h2 = dict_h[d.label][s.label][reg][v._name].GetValue()
                merge_UnOvFlow2D(h2)
                if isMC:
                    h2.Scale(s.sigma*10**3/ntot_events[d.label][s.label])
                outfile.cd()
                h2.Write()
        outfile.Close()
