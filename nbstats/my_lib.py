import zipfile
import json
import re
import nbstats


def check_notebooks_within_zipfile(zipfile_path):
    """
    Return list of notebooks within a zipfile
    """
    with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
        files = zip_ref.namelist()
    files = [f for f in files if f.endswith('.ipynb')]
    return files


def get_student_name(filename: str):
    student_name = filename.split('_')[1]
    return student_name


def open_notebook_from_zip(zipfile_path, notebook_name):
    """
    Open a notebook from a zipfile
    """
    with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
        with zip_ref.open(notebook_name) as file:
            nb = json.load(file)
    return nb


def evaluate_notebook(nb: dict, nb_ref: dict):
    """
    Evaluate a notebook
    """
    similarity, mean_code_difference, total_code_difference = nbstats.typical_nonzero_similarity(
        nb, nb_ref)
    return similarity, mean_code_difference, total_code_difference


def evaluate_zipfile(zipfile_path, reference_path):
    """
    Evaluate a zipfile
    """
    files = check_notebooks_within_zipfile(zipfile_path)
    with open(reference_path, 'r') as file:
        nb_ref = json.load(file)

    results = []
    for f in files:
        nb = open_notebook_from_zip(zipfile_path, f)
        similarity, mean_code_difference, total_code_difference = evaluate_notebook(
            nb, nb_ref)
        this_result = {
            'student_name': get_student_name(f),
            'similarity': similarity,
            'mean_code_difference': mean_code_difference,
            'total_code_difference': total_code_difference
        }
        results.append(this_result)
    return results


def extract_code_cells(nb: dict):
    code_cells = []
    for cell in nb['cells']:
        if 'cell_type' in cell.keys():
            if cell['cell_type'] == 'code':
                code_cells.append(cell)
    return code_cells


def filter_empty_code(code):
    ret = [c for c in code if not re.match(r'^\s*$', c)]
    return ret
