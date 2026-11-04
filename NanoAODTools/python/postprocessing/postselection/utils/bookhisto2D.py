def bookhisto2D(df, regions_def, var2d, s_cut, weight):
    # weight: name of the column used as event weight
    h_ = {}
    # for reg in ["SR"]:
    #     h_[reg] = {}
    #     for v in var2d:
    v = var2d[0]
    h_["incl"] = {}
            # if regions_def[reg]=="":
            #     h_[reg][v._name] = df.Redefine(v._xname, "UnOvBin("+v._xname+","+str(v._nxbins)+","+str(v._xmin)+","+str(v._xmax)+")")\
            #                          .Redefine(v._yname, "UnOvBin("+v._yname+","+str(v._nybins)+","+str(v._ymin)+","+str(v._ymax)+")")\
            #                          .Histo2D((v._xname+"Vs"+v._yname+"_"+reg+"_"+s_cut," ;"+v._xtitle+";"+v._ytitle, v._nxbins, v._xmin, v._xmax, v._nybins, v._ymin, v._ymax), v._xname, v._yname)
            # else:
            #     h_[reg][v._name] = df.Filter(regions_def[reg])\
            #                          .Redefine(v._xname, "UnOvBin("+v._xname+","+str(v._nxbins)+","+str(v._xmin)+","+str(v._xmax)+")")\
            #                          .Redefine(v._yname, "UnOvBin("+v._yname+","+str(v._nybins)+","+str(v._ymin)+","+str(v._ymax)+")")\
            #                          .Histo2D((v._xname+"Vs"+v._yname+"_"+reg+"_"+s_cut," ;"+v._xtitle+";"+v._ytitle, v._nxbins, v._xmin, v._xmax, v._nybins, v._ymin, v._ymax), v._xname, v._yname)
    h_["incl"][v._name+"_0TopMer"] = df.Filter("nTightTopMerged==0")\
                                    .Histo2D((v._xname+"Vs"+v._yname+"_"+"incl_0TopMer"," ;"+v._xtitle+";"+v._ytitle, v._nxbins, v._xmin, v._xmax, v._nybins, v._ymin, v._ymax), v._xname, v._yname, weight)
    h_["incl"][v._name+"_1TopMer"] = df.Filter("nTightTopMerged>0")\
                                    .Histo2D((v._xname+"Vs"+v._yname+"_"+"incl_1TopMer"," ;"+v._xtitle+";"+v._ytitle, v._nxbins, v._xmin, v._xmax, v._nybins, v._ymin, v._ymax), v._xname, v._yname, weight)
    return h_
