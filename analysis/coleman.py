
from utils import load_corpora, print_kolmogorov

SNL_PATH = '../../text_complexity/data/SNL/snl_coleman.json'  # Dictionary
NAK_PATH = '../../text_complexity/data/NAK_2019/nak_coleman.json'  # Newspaper
ST_PATH = '../../text_complexity/data/ST/st_coleman.json'  # Legislations

if __name__ == '__main__':
    snl_data = load_corpora(SNL_PATH)
    nak_data = load_corpora(NAK_PATH)
    st_data = load_corpora(ST_PATH)

    print_kolmogorov('coleman_kolmogorov_nak_snl', nak_data, snl_data)
    print_kolmogorov('coleman_kolmogorov_nak_st', nak_data, st_data)
    print_kolmogorov('coleman_kolmogorov_snl_st', snl_data, st_data)
