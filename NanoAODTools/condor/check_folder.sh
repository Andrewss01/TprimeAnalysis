#!/bin/bash
PROXY="/tmp/x509up_u180940"
CAPATH="/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates"
BASE="davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/Run3Analysis_Tprime/Eval_samples"
davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE" 
# print("davix-ls -E", PROXY , "--capath" , CAPATH , BASE)
