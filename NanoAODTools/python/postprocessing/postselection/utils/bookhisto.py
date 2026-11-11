from PhysicsTools.NanoAODTools.postprocessing.postselection.utils.split_cuts_keeping_parentheses import split_cuts_keeping_parentheses

def bookhisto(df, regions_def, var, s_cut, weight, sampleflag, printcutflow):
    # weight: name of the column used as event weight (regions with "NoPu" in the name are not weighted)
    h_ = {}
    for reg in regions_def.keys():
        h_[reg] = {}
        for v in var:
            if v._MConly and not sampleflag:
                continue
            else:
                # print(v._name+"_"+reg+"_"+s_cut)
                if regions_def[reg] == "":
                    if "NoPu" in reg:
                        h_[reg][v._name]= df.Histo1D((v._name+"_"+reg," ;"+v._title+"", v._nbins, v._xmin, v._xmax), v._name)
                    else:
                        h_[reg][v._name]= df.Histo1D((v._name+"_"+reg," ;"+v._title+"", v._nbins, v._xmin, v._xmax), v._name, weight)
                else:
                    if "NoPu" in reg:
                        h_[reg][v._name]= df.Filter(regions_def[reg]).Histo1D((v._name+"_"+reg," ;"+v._title+"", v._nbins, v._xmin, v._xmax), v._name)
                    else:
                        h_[reg][v._name]= df.Filter(regions_def[reg]).Histo1D((v._name+"_"+reg," ;"+v._title, v._nbins, v._xmin, v._xmax), v._name, weight)
        if printcutflow and reg == 'SRTop':
            cuts = split_cuts_keeping_parentheses(regions_def[reg])
            # print("Cutflow for region {}:".format(reg))
            # print(cuts)
            print("Cutflow for region {}:".format(reg))
            df_cutflow = df
            for cut in cuts:
                df_cutflow = df_cutflow.Filter(cut, cut)
            df_cutflow.Report().Print()
    return h_
