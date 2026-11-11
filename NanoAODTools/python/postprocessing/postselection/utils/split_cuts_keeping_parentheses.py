def split_cuts_keeping_parentheses(cut_string):
    """
    Splits a cut string by '&&' while keeping parenthesized expressions together.
    Example: "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon==0) && nJetBtagLoose>0"
    Returns: ["PuppiMET_T1_pt_nominal>250", "MinDelta_phi>0.6", "(nVetoElectron==0 && nVetoMuon==0)", "nJetBtagLoose>0"]
    """
    cuts = []
    current_cut = ""
    paren_depth = 0

    i = 0
    while i < len(cut_string):
        char = cut_string[i]

        if char == '(':
            paren_depth += 1
            current_cut += char
        elif char == ')':
            paren_depth -= 1
            current_cut += char
        elif char == '&' and i + 1 < len(cut_string) and cut_string[i + 1] == '&' and paren_depth == 0:
            # Found '&&' at depth 0, so this is a cut separator
            cuts.append(current_cut.strip())
            current_cut = ""
            i += 1  # Skip the second '&'
        else:
            current_cut += char

        i += 1

    # Add the last cut
    if current_cut.strip():
        cuts.append(current_cut.strip())

    return cuts
