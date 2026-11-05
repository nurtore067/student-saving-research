"""Execute analysis; --measure replaces timings with new measurements."""
import argparse
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from src.task3_benchmark import main as benchmark

ROOT = Path(__file__).resolve().parent


def execute_in_process(notebook):
    # Restricted execution hosts may disallow the sockets required by Jupyter.
    # A fresh Python process can still execute the actual cells using IPython.
    from IPython.core.interactiveshell import InteractiveShell
    from IPython.utils.capture import capture_output
    shell = InteractiveShell.instance()
    for cell in notebook.cells:
        if cell.cell_type != 'code':
            continue
        count = shell.execution_count
        with capture_output() as captured:
            result = shell.run_cell(cell.source, store_history=True)
        if result.error_before_exec or result.error_in_exec:
            raise RuntimeError(str(result.error_before_exec or result.error_in_exec))
        cell.execution_count = count
        cell.outputs = []
        if captured.stdout:
            cell.outputs.append(nbformat.v4.new_output('stream', name='stdout', text=captured.stdout))
        if captured.stderr:
            cell.outputs.append(nbformat.v4.new_output('stream', name='stderr', text=captured.stderr))
        for output in captured.outputs:
            cell.outputs.append(nbformat.v4.new_output('display_data', data=output.data, metadata=output.metadata))
    notebook.metadata['execution_note'] = 'Cells actually executed in order in a fresh Python process using IPython. Separate Jupyter kernel sockets unavailable on authoring host.'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--measure', action='store_true')
    parser.add_argument('--in-process', action='store_true', help='Use IPython when kernel sockets are unavailable')
    args = parser.parse_args()
    if args.measure:
        benchmark()
    path = ROOT/'notebooks/01_data_analysis.ipynb'
    notebook = nbformat.read(path, as_version=4)
    if args.in_process:
        execute_in_process(notebook)
    else:
        NotebookClient(notebook, timeout=180, kernel_name='python3', resources={'metadata': {'path':str(ROOT)}}).execute()
        notebook.metadata['execution_note'] = 'Executed with nbclient in a fresh Jupyter kernel.'
    nbformat.write(notebook,path)
    print('Notebook executed; CSV, figures and Markdown report refreshed.')
