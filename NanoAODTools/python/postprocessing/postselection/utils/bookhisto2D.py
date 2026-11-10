import ROOT
import numpy as np

def bin_edges(nbins, xmin, xmax, xarray):
    # bin edges of one axis of a variable2D: xarray if given, otherwise nbins uniform bins in [xmin, xmax]
    if xarray is not None:
        return np.array(xarray, dtype='d')
    return np.linspace(xmin, xmax, nbins+1, dtype='d')

def model2D(v, reg):
    # TH2D model of the variable2D v in the region reg (named as the 1D histograms: <variable>_<region>)
    xedges = bin_edges(v._nxbins, v._xmin, v._xmax, v._xarray)
    yedges = bin_edges(v._nybins, v._ymin, v._ymax, v._yarray)
    return ROOT.RDF.TH2DModel(v._name+"_"+reg, " ;"+v._xtitle+";"+v._ytitle, len(xedges)-1, xedges, len(yedges)-1, yedges)

def bookhisto2D(df, regions_def, var2d, weight):
    # books one TH2D for every region and every variable2D: h_[reg][v._name]
    # regions_def[reg] is the cut of the region ("" = no cut); weight is the name of the event weight column.
    # Under/overflow is left in the flow bins here and folded into the edge bins by savehisto2d.
    h_ = {}
    for reg in regions_def.keys():
        h_[reg] = {}
        if regions_def[reg] == "":
            df_reg = df
        else:
            df_reg = df.Filter(regions_def[reg])
        for v in var2d:
            h_[reg][v._name] = df_reg.Histo2D(model2D(v, reg), v._xname, v._yname, weight)
    return h_
