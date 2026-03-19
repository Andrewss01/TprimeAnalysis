#!/bin/bash
PROXY="/tmp/x509up_u180940"
CAPATH="/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates"
BASE="davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/Run3Analysis_Tprime/TprimeToTZ_900_2022/20260219_171555/"
davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE"
print("davix-ls -E", PROXY , "--capath" , CAPATH , BASE)
