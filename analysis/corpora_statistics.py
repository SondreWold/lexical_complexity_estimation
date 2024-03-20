import matplotlib.pyplot as plt
import json
from statistics import stdev, variance, mean
from utils import load_corpora, print_kolmogorov

SNL_PATH = '../../text_complexity/data/SNL/snl_lix.json'  # Dictionary
NAK_PATH = '../../text_complexity/data/NAK_2019/nak_lix_all.json'  # Newspaper
ST_PATH = '../../text_complexity/data/ST/st_lix.json'  # Legislations
CH_PATH = '../../text_complexity/data/BARN/barnebok_liks.json'  # Childrens books


def print_desc_statistics(name, values):
    result = {
        'mean': mean(values),
        'variance': variance(values),
        'std.dev': stdev(values)
    }
    with open(f"./outputs/{name}.json", "w") as outfile:
        json.dump(result, outfile)


if __name__ == '__main__':
    snl_data = load_corpora(SNL_PATH)
    nak_data = load_corpora(NAK_PATH)
    st_data = load_corpora(ST_PATH)
    children_data = load_corpora(CH_PATH)
    total_data = snl_data + nak_data + st_data + children_data

    print_desc_statistics('descriptives_SNL', snl_data)
    print_desc_statistics('descriptives_NAK', nak_data)
    print_desc_statistics('descriptives_ST', st_data)
    print_desc_statistics('descriptives_CH', children_data)
    print_desc_statistics('descriptives_TOTAL', total_data)

    print_kolmogorov('kolmogorov_ch_nak', children_data, nak_data)
    print_kolmogorov('kolmogorov_ch_snl', children_data, snl_data)
    print_kolmogorov('kolmogorov_ch_st', children_data, st_data)
    print_kolmogorov('kolmogorov_nak_snl', nak_data, snl_data)
    print_kolmogorov('kolmogorov_nak_st', nak_data, st_data)
    print_kolmogorov('kolmogorov_snl_st', snl_data, st_data)

    plt.figure(figsize=(14, 7))
    plt.hist(children_data, label='Children', alpha=.7, bins='auto', density=True)
    plt.hist(nak_data, label='News', alpha=.5, bins='auto', density=True)
    plt.hist(snl_data, label='Encyclopedia', alpha=.7, bins='auto', density=True)
    plt.hist(st_data, label='Law', alpha=.6, bins='auto', density=True)
    plt.xlabel("LIX", fontsize=20)
    plt.xticks(fontsize=18)
    plt.ylabel("Density", fontsize=20)
    plt.yticks(fontsize=14)
    plt.legend(prop={'size': 18})
    plt.grid(False)
    plt.savefig("./outputs/corpora.pdf", format="pdf", bbox_inches="tight")
