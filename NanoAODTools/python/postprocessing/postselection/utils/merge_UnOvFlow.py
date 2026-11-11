import math

def merge_UnOvFlow(h):
    # underflow added to the first bin and overflow to the last one (errors in quadrature);
    # the underflow and overflow bins themselves are left as they are
    nbins = h.GetNbinsX()
    h.SetBinContent(1, h.GetBinContent(0) + h.GetBinContent(1))
    h.SetBinError(1, math.sqrt(pow(h.GetBinError(0),2) + pow(h.GetBinError(1),2)))
    h.SetBinContent(nbins, h.GetBinContent(nbins) + h.GetBinContent(nbins+1))
    h.SetBinError(nbins, math.sqrt(pow(h.GetBinError(nbins),2) + pow(h.GetBinError(nbins+1),2)))


def merge_UnOvFlow2D(h):
    # 2D version: the content of every under/overflow bin (in x, in y or in both) is added to the nearest
    # bin inside the axes (errors in quadrature), then the under/overflow bin is set to zero.
    # Unlike merge_UnOvFlow, the flow bins are cleared: TH2::ProjectionX/Y include them by default,
    # so leaving them would count those events twice in the projections.
    nx = h.GetNbinsX()
    ny = h.GetNbinsY()
    for i in range(0, nx+2):
        for j in range(0, ny+2):
            i_in = min(max(i, 1), nx)
            j_in = min(max(j, 1), ny)
            if i_in == i and j_in == j:
                continue
            content = h.GetBinContent(i, j)
            error   = h.GetBinError(i, j)
            h.SetBinContent(i_in, j_in, h.GetBinContent(i_in, j_in) + content)
            h.SetBinError(i_in, j_in, math.sqrt(pow(h.GetBinError(i_in, j_in),2) + pow(error,2)))
            h.SetBinContent(i, j, 0.)
            h.SetBinError(i, j, 0.)
