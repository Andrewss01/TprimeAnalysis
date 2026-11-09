import math
import numpy as np
from PhysicsTools.NanoAODTools.postprocessing.postselection.utils.variable import variable, variable2D    # classes in postselection/utils/variable.py


### Definition of requeriments for plots (cut), variables and regions

requirements = ""

######## 1D variables for histos

vars = []

vars.append(variable(name = "TopResolved_TopScore_nominal",         title= "Top Resolved Score",            nbins = 40, xmin = 0, xmax=1, noUnOvFlowbin = True))
vars.append(variable(name = "TopMixed_TopScore_nominal",            title= "Top Mixed Score",               nbins = 40, xmin = 0, xmax=1, noUnOvFlowbin = True))
vars.append(variable(name = "TopMerged_TopScore_nominal",           title= "Top Merged Score",              nbins = 40, xmin = 0, xmax=1, noUnOvFlowbin = True))

# Fine binning (0.0001) to find the working points down to 1% mistag (draw_WorkingPoints.py): with 40 bins (0.025) the 1% of Mixed falls in the last bin.
# 10000 bins is an exact refinement of the old 40 bins (Rebin(250) gives them back), used for the 10%/5% WPs in TopTagging_WorkingPoints.json
vars.append(variable(name = "BestTopResolved_score",                title= "Best Top Resolved Score",       nbins = 10000, xmin = 0, xmax=1, noUnOvFlowbin = True))
vars.append(variable(name = "BestTopMixed_score",                   title= "Best Top Mixed Score",          nbins = 10000, xmin = 0, xmax=1, noUnOvFlowbin = True))
vars.append(variable(name = "BestTopMerged_score",                  title= "Best Top Merged Score",         nbins = 10000, xmin = 0, xmax=1, noUnOvFlowbin = True))


######## 2D variables for histos
vars2D = []



#### REGIONS DEFINITION ####

regions = {

    "presel"                            : "",
    "BestTopResolved_topmatched"        : "BestTopResolved_process==0",
    "BestTopResolved_nonmatched"        : "BestTopResolved_process==1",
    "BestTopResolved_other"             : "BestTopResolved_process==2",
    "BestTopMixed_topmatched"           : "BestTopMixed_process==0",
    "BestTopMixed_nonmatched"           : "BestTopMixed_process==1",
    "BestTopMixed_other"                : "BestTopMixed_process==2",
    "BestTopMerged_topmatched"          : "BestTopMerged_process==0",
    "BestTopMerged_nonmatched"          : "BestTopMerged_process==1",
    "BestTopMerged_other"               : "BestTopMerged_process==2",
    "btagSFcheck"                       : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon==0)",

    }