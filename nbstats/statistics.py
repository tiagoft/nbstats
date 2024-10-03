import nbstats
import re
import numpy as np

def number_of_copies(nb_eval : dict, nb_ref : dict):
    code_cells_eval = nbstats.extract_code_cells(nb_eval)
    code_cells_ref = nbstats.extract_code_cells(nb_ref)
    similarity = 0
    for cell1 in code_cells_ref:
        for cell2 in code_cells_eval:
            c1, c2 = cell1['source'], cell2['source']
            if c1 == c2:
                similarity += 1
                break
    return similarity

def count_different_lines(code_eval : str, reference_path : str):
    return len([l for l in code_eval if l not in reference_path and not l.startswith('#') and not re.search(r'^#*\s*$', l)])

def typical_nonzero_similarity(nb_eval, nb_ref):
    code_cells_eval = nbstats.extract_code_cells(nb_eval)
    code_cells_ref = nbstats.extract_code_cells(nb_ref)
    similarity = 0
    code_differences = []
    for cell1 in code_cells_ref:
        code_difference = 900000
        for cell2 in code_cells_eval:
            if cell1['source'] == cell2['source']:
                similarity += 1
                code_difference = 0
                break
            else:
                different_lines = count_different_lines(cell1['source'], cell2['source'])
                if different_lines < code_difference:
                    code_difference = different_lines
        if code_difference > 0:
            code_differences.append(code_difference)
    if len(code_differences) == 0:
        mean_code_difference = 0
    else:
        mean_code_difference = np.mean(code_differences)
    
    total_code_difference = np.sum(code_differences)
    return similarity, mean_code_difference, total_code_difference