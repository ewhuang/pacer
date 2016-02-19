### Author: Edward Huang

from collections import OrderedDict

### This script summarizes the compare_lincs_Aft_NUM_and_method_hgnc.txt files
### with the following table format:
### threshold/fisher-p  0.001 0.005 0.01 0.05 0.1
### 0.001
### 0.005
### ...

fisher_p_range = [0.001, 0.005, 0.01, 0.05, 0.1]
threshold_range = [0.0001, 0.001, 0.01, 0.05]

def summarize_file_and_write(in_filename):
    f = open(in_filename, 'r')
    table_dct = OrderedDict({})
    for i, line in enumerate(f):
        # Skip the header line.
        if i == 0:
            continue
        line = line.split()
        threshold, fisher_p = float(line[0]), float(line[-1])
        for fisher_p_thresh in fisher_p_range:
            if fisher_p < fisher_p_thresh:
                if (threshold, fisher_p_thresh) in table_dct:
                    table_dct[(threshold, fisher_p_thresh)] += 1
                else:
                    table_dct[(threshold, fisher_p_thresh)] = 1
    f.close()

    ### This threshold range definition has duplicate thresholds. Use the
    ### hardcoded one for now.
    # threshold_range = [threshold for threshold, fisher_p_thresh in table_dct]
    
    out = open(in_filename[:10] + 'summ_' + in_filename[10:], 'w')
    out.write('\t' + '\t'.join(map(str, fisher_p_range)) + '\n')
    for threshold in threshold_range:
        out.write(str(threshold))
        for fisher_p in fisher_p_range:
            if (threshold, fisher_p) not in table_dct:
                out.write('\t0')
            else:
                out.write('\t%d' % table_dct[(threshold, fisher_p)])
        out.write('\n')
    out.close()


if __name__ == '__main__':
    # Expression summaries.
    base = './results/compare_lincs_Aft_3_and_'
    exp_fname = base + 'exp_hgnc.txt'
    summarize_file_and_write(exp_fname)

    # Embedding summaries.
    for top_k in [250]: # TODO
        for num in [50, 100, 500, 1000, 1500, 2000]:
            num = str(num)
            for suffix in ['U', 'US']:
                entity_vector_dct = OrderedDict({})

                extension = '%s_0.8.%s' % (num, suffix)
                embedding_fname = base + extension + '_top_%d_hgnc.txt' % (top_k)
                summarize_file_and_write(embedding_fname)

    # L1 summaries.
    l1_fname = base + 'l1_hgnc.txt'
    summarize_file_and_write(l1_fname)

    # Compare the expression summaries with embedding summaries.
    exp_file = open('./results/summ_compare_lincs_Aft_3_and_exp_hgnc.txt', 'r')
    exp_table = []
    for i, line in enumerate(exp_file):
        if i == 0:
            continue
        line = map(float, line.split())[1:]
        exp_table += line
    exp_file.close()

    # Get the embedding summaries.
    for top_k in [250]: # TODO
        for num in [50, 100, 500, 1000, 1500, 2000]:
            num = str(num)
            for suffix in ['U', 'US']:
                entity_vector_dct = OrderedDict({})

                extension = '%s_0.8.%s' % (num, suffix)
                embedding_fname = './results/summ_compare_lincs_Aft_3_and_' + extension + '_top_%d_hgnc.txt' % (top_k)
                
                embedding_table = []
                f = open(embedding_fname, 'r')
                for i, line in enumerate(f):
                    if i == 0:
                        continue
                    line = map(float, line.split())[1:]
                    embedding_table += line
                f.close()
                num_better_than_expresion = 0
                for i, val in enumerate(embedding_table):
                    if val > exp_table[i]:
                        num_better_than_expresion += 1
                if num_better_than_expresion > 8:
                    print embedding_fname