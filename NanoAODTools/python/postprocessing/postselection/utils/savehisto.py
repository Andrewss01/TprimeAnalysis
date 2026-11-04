import ROOT
from PhysicsTools.NanoAODTools.postprocessing.postselection.utils.merge_UnOvFlow import merge_UnOvFlow

def savehisto(d, dict_h, regions_def, var, s_cut, outfile_dict, variations, do_variations, ntot_events):
    # dict_h[d.label][s.label][reg][var]: booked histograms (RResultMap of the variations if do_variations)
    # MC histograms are normalized to sigma*10**3/ntot_events[d.label][s.label]
    histo = {reg: {v._name: ROOT.TH1D(v._name+"_"+reg+"_"+s_cut," ;"+v._title+"", v._nbins, v._xmin, v._xmax) for v in var} for reg in regions_def.keys()}
    isMC=True
    if "Data" in d.label: isMC = False
    if hasattr(d, "components"):
        s_list = d.components
    else:
        s_list = [d]

    for s in s_list:
        outfile_path    = outfile_dict[s.label]
        outfile         = ROOT.TFile.Open(outfile_path, "RECREATE")
        for n, vari in enumerate(variations):
            for reg in regions_def.keys():
                for v in var:
                    if "SFbtag" in v._name: continue
                    if v._MConly and not isMC:
                        continue
                    else:
                        # da capire come fare il getvalue e dividere le variazioni
                        if isMC:
                            if do_variations:
                                if vari=='nominal':
                                    h1 = dict_h[d.label][s.label][reg][v._name]["nominal"]
                                    h1.SetName(h1.GetName()+"_nominal")
                                    if not v._noUnOvFlowbin:
                                        merge_UnOvFlow(h1)
                                    if isMC:
                                        h1.Scale(s.sigma*10**3/ntot_events[d.label][s.label])
                                    histo_name = h1.GetName()
                                    if "nominal" not in histo_name : h1.SetName(histo_name+"_nominal")
                                    outfile.cd()
                                    h1.Write()
                                elif vari=="pdf_total":
                                    hnom = dict_h[d.label][s.label][reg][v._name]["nominal"]
                                    hup = dict_h[d.label][s.label][reg][v._name][vari+":up"]
                                    hdown = dict_h[d.label][s.label][reg][v._name][vari+":down"]
                                    hup.SetName(hup.GetName())
                                    hdown.SetName(hdown.GetName())
                                    if not v._noUnOvFlowbin:
                                        merge_UnOvFlow(hup)
                                        merge_UnOvFlow(hdown)
                                    if isMC:
                                        hup.Scale(s.sigma*10**3/ntot_events[d.label][s.label])
                                        hdown.Scale(s.sigma*10**3/ntot_events[d.label][s.label])
                                        if hup.Integral()>0 and hdown.Integral()>0:
                                            hup.Scale((hnom.Integral()+(hup.Integral()-hdown.Integral()))/hup.Integral())
                                            hdown.Scale((hnom.Integral()-(hup.Integral()-hdown.Integral()))/hdown.Integral())
                                    outfile.cd()
                                    hup.Write()
                                    hdown.Write()
                                else:
                                    for var_type in ['up', 'down']:
                                        if f"{vari}:{var_type}" not in dict_h[d.label][s.label][reg][v._name].GetKeys():
                                            continue
                                        h1 = dict_h[d.label][s.label][reg][v._name][vari+":"+var_type]
                                        # h1.SetName(h1.GetName()+"_"+vari+var_type.capitalize())
                                        histo_name = h1.GetName()
                                        if vari+"_"+var_type not in histo_name:
                                            h1.SetName(h1.GetName()+"_"+vari+"_"+var_type)
                                        if not v._noUnOvFlowbin:
                                            merge_UnOvFlow(h1)

                                        if isMC:
                                            h1.Scale(s.sigma*10**3/ntot_events[d.label][s.label])
                                        outfile.cd()
                                        h1.Write()
                            else:
                                histo[reg][v._name] = dict_h[d.label][s.label][reg][v._name].GetValue()
                                if not v._noUnOvFlowbin:
                                    merge_UnOvFlow(histo[reg][v._name])
                                if isMC:
                                    histo[reg][v._name].Scale(s.sigma*10**3/ntot_events[d.label][s.label])
                                outfile.cd()
                                histo[reg][v._name].Write()
                        else:
                            histo[reg][v._name] = dict_h[d.label][s.label][reg][v._name].GetValue()
                            if not v._noUnOvFlowbin:
                                merge_UnOvFlow(histo[reg][v._name])
                            if isMC:
                                histo[reg][v._name].Scale(s.sigma*10**3/ntot_events[d.label][s.label])
                            outfile.cd()
                            histo[reg][v._name].Write()
        outfile.Close()
