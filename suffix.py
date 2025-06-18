def build_suffix_array(text):
    return sorted([text[i:] for i in range(len(text))])

def build_lcp_array(suffix_array):
    # Aqui você pode implementar a LCP array com base nos suffixes
    pass
