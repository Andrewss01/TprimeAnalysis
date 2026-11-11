import sys

# weights that can be removed from the event weight: option name -> column in the RDataFrame
# the order is the one of the names in the output folders
REMOVABLE_WEIGHTS = {
    "noSFbtag":         "SFbtag_nominal",
    "noPuWeight":       "puWeight",
    "noTopPtWeight":    "w_topPt",
    "noTrotaSF":        "TotalTrotaEventWeight",
}
ALL_WEIGHTS = "allWeights"

def parse_weightsets(weightset_args, global_removed):
    # weightset_args: values of the --weightset options (None if not given), e.g. ["allWeights", "noSFbtag", "noSFbtag,noTrotaSF"]
    # global_removed: names of the --noXXX options given, removed from every weightset
    # returns [(label, removed)] with removed the set of names removed in that weightset (global ones included)
    # and label the removed names in the order of REMOVABLE_WEIGHTS joined by "_" ("allWeights" if none),
    # used as name of the output folder of the weightset
    if weightset_args is None:
        weightset_args = [ALL_WEIGHTS]
    weightsets = []
    for arg in weightset_args:
        names = [n.strip() for n in arg.split(",")]
        if ALL_WEIGHTS in names and len(names) > 1:
            sys.exit(f"ERROR: --weightset {arg}: {ALL_WEIGHTS} cannot be combined with other names")
        removed = set(global_removed)
        for n in names:
            if n == ALL_WEIGHTS:
                continue
            if n not in REMOVABLE_WEIGHTS:
                sys.exit(f"ERROR: --weightset {arg}: unknown name {n}, valid names: {ALL_WEIGHTS}, " + ", ".join(REMOVABLE_WEIGHTS))
            if n in global_removed:
                sys.exit(f"ERROR: --weightset {arg}: {n} already removed from every weightset with --{n}")
            removed.add(n)
        label = "_".join(n for n in REMOVABLE_WEIGHTS if n in removed) or ALL_WEIGHTS
        if label in [l for l, _ in weightsets]:
            sys.exit(f"ERROR: --weightset {arg}: weightset {label} given twice")
        weightsets.append((label, removed))
    return weightsets
