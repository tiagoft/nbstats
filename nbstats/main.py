import nbstats
import os
from pathlib import Path
from rich.console import Console
import typer
import pandas as pd

app = typer.Typer(no_args_is_help=True)
console = Console()

@app.command('version')
def print_version():
    """
    Print information about the module
    """
    console.print(f"nbstats\nAuthor: { nbstats.__author__}")
    console.print(f"Version: { nbstats.__version__}")

@app.command('check')
def check(zipfile_path : str):
    """
    List all notebooks within a zipfile
    """
    files = nbstats.check_notebooks_within_zipfile(zipfile_path)
    for f in files:
        console.print(f)

@app.command() # Defines a default action
def eval(zipfile_path : str, reference_path : str):
    """
    Evaluates a zipfile with notebooks
    """
    results = nbstats.evaluate_zipfile(zipfile_path, reference_path)
    df = pd.DataFrame(results)
    console.print(df)

if __name__ == "__main__":
    app()