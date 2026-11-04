import ROOT

# i plot2d per il momento non ci servono, si deve trovare un modo più intelligente di farli
def savehisto2d(d, h, regions_def, var2d, s_cut, outfolder, do_variations):
    # outfolder: folder where <sample>_2D.root is written
    # histo = {reg: {v._name: ROOT.TH2D(v._name+"_"+reg+"_"+s_cut," ;"+v._xtitle+";"+v._ytitle, v._nxbins, v._xmin, v._xmax, v._nybins, v._ymin, v._ymax,) for v in var2d} for reg in regions_def.keys()}
    histo = {'incl': {
        'nTopMixedVsnTopResolved_0TopMer': ROOT.TH2D('nTopMixedVsnTopResolved_0TopMer_SR', ' ;Number of TopResolved;Number of TopMixed', 6, -0.5, 5.5, 6, -0.5, 5.5),
        'nTopMixedVsnTopResolved_1TopMer': ROOT.TH2D('nTopMixedVsnTopResolved_1TopMer_SR', ' ;Number of TopResolved;Number of TopMixed', 6, -0.5, 5.5, 6, -0.5, 5.5)
    }}

    if hasattr(d, "components"):
        s_list = d.components
    else:
        s_list = [d]

    for s in s_list:
        outfile = ROOT.TFile.Open(outfolder+s.label+'_2D.root', "RECREATE")
        # for reg in regions_def.keys():
        #     for v in histo[reg].keys():
        #         histo[reg][v] = h[d.label][s.label][reg][v].GetValue()
        #         if isMC:
        #             histo[reg][v._name].Scale(s.sigma*10**3/ntot_events[d.label][s.label])
        #         outfile.cd()
        #         histo[reg][v].Write()
        if do_variations:
            histo['incl']['nTightTopMixedVsnTightTopResolved_0TopMer'] = h[d.label][s.label]['incl']['nTightTopMixedVsnTightTopResolved_0TopMer']["nominal"]
            histo['incl']['nTightTopMixedVsnTightTopResolved_1TopMer'] = h[d.label][s.label]['incl']['nTightTopMixedVsnTightTopResolved_1TopMer']["nominal"]
        else:
            histo['incl']['nTightTopMixedVsnTightTopResolved_0TopMer'] = h[d.label][s.label]['incl']['nTightTopMixedVsnTightTopResolved_0TopMer'].GetValue()
            histo['incl']['nTightTopMixedVsnTightTopResolved_1TopMer'] = h[d.label][s.label]['incl']['nTightTopMixedVsnTightTopResolved_1TopMer'].GetValue()

        # histo['incl']['nTightTopMixedVsnTightTopResolved_0TopMer'].Scale(s.sigma*10**3/ntot_events[d.label][s.label])
        # histo['incl']['nTightTopMixedVsnTightTopResolved_1TopMer'].Scale(s.sigma*10**3/ntot_events[d.label][s.label])
        histo['incl']['nTightTopMixedVsnTightTopResolved_0TopMer'].Write()
        histo['incl']['nTightTopMixedVsnTightTopResolved_1TopMer'].Write()
        outfile.Close()
