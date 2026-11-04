import math

def merge_UnOvFlow(h):
    # underflow added to the first bin and overflow to the last one (errors in quadrature);
    # the underflow and overflow bins themselves are left as they are
    nbins = h.GetNbinsX()
    h.SetBinContent(1, h.GetBinContent(0) + h.GetBinContent(1))
    h.SetBinError(1, math.sqrt(pow(h.GetBinError(0),2) + pow(h.GetBinError(1),2)))
    h.SetBinContent(nbins, h.GetBinContent(nbins) + h.GetBinContent(nbins+1))
    h.SetBinError(nbins, math.sqrt(pow(h.GetBinError(nbins),2) + pow(h.GetBinError(nbins+1),2)))
