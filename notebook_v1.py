#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
an object-oriented version of the notebook toolbox
"""
from notebook_v0 import get_cells, get_format_version, load_ipynb, save_ipynb, to_percent

class Cell :
    def __init__(self,ipynb):
        self.id = ipynb['id']
        self.source = ipynb['source']

class CodeCell(Cell):
    r"""A Cell of Python code in a Jupyter notebook.

    Args:
        ipynb (dict): a dictionary representing the cell in a Jupyter Notebook.

    Attributes:
        id (int): the cell's id.
        source (list): the cell's source code, as a list of str.
        execution_count (int): number of times the cell has been executed.

    Usage:

        >>> code_cell = CodeCell({
        ...     "cell_type": "code",
        ...     "execution_count": 1,
        ...     "id": "b777420a",
        ...     'source': ['print("Hello world!")']
        ... })
        >>> code_cell.id
        'b777420a'
        >>> code_cell.execution_count
        1
        >>> code_cell.source
        ['print("Hello world!")']
    """

    def __init__(self, ipynb):
        #self.id = ipynb['id']
        #self.source = ipynb['source']
        super().__init__(ipynb)
        self.execution_count = ipynb['execution_count']
    

class MarkdownCell(Cell):  # (Cell) signifie que la classe Markdown hérite de tout ce qu'il y a dans la class parente Cell
    r"""A Cell of Markdown markup in a Jupyter notebook.

    Args:
        ipynb (dict): a dictionary representing the cell in a Jupyter Notebook.

    Attributes:
        id (int): the cell's id.
        source (list): the cell's source code, as a list of str.

    Usage:

        >>> markdown_cell = MarkdownCell({
        ...    "cell_type": "markdown",
        ...    "id": "a9541506",
        ...    "source": [
        ...        "Hello world!\n",
        ...        "============\n",
        ...        "Print `Hello world!`:"
        ...    ]
        ... })
        >>> markdown_cell.id
        'a9541506'
        >>> markdown_cell.source
        ['Hello world!\n', '============\n', 'Print `Hello world!`:']
    """

    def __init__(self, ipynb):      
        #self.id = ipynb['id']
        #self.source = ipynb['source']
        super().__init__(ipynb)

class Notebook:
    r"""A Jupyter Notebook.

    Args:
        ipynb (dict): a dictionary representing a Jupyter Notebook.

    Attributes:
        version (str): the version of the notebook format.
        cells (list): a list of cells (either CodeCell or MarkdownCell).

    Usage:

        - checking the verion number:

            >>> ipynb = toolbox.load_ipynb("samples/minimal.ipynb")
            >>> nb = Notebook(ipynb)
            >>> nb.version
            '4.5'

        - checking the type of the notebook parts:

            >>> ipynb = toolbox.load_ipynb("samples/hello-world.ipynb")
            >>> nb = Notebook(ipynb)
            >>> isinstance(nb.cells, list)
            True
            >>> isinstance(nb.cells[0], Cell)
            True
    """

    def __init__(self, ipynb):
        self.version = get_format_version(ipynb)
        cell = []
        for c in get_cells(ipynb):
            if c['cell_type'] == 'markdown':
                cell.append(MarkdownCell(c))
            elif c['cell_type'] == 'code':
                cell.append(CodeCell(c))
        self.cells = cell 
        self.ipynb = ipynb 


    @staticmethod
    def from_file(filename):
        r"""Loads a notebook from an .ipynb file.

        Usage:

            >>> nb = Notebook.from_file("samples/minimal.ipynb")
            >>> nb.version
            '4.5'
        """
        return Notebook(load_ipynb(filename))  

    def __iter__(self):
        r"""Iterate the cells of the notebook.

        Usage:

            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> for cell in nb:
            ...     print(cell.id)
            a9541506
            b777420a
            a23ab5ac
        """
        return iter(self.cells)


#Pour que la question suivante fonctionne, il faut redéfinir la fonction to_percent car celle du notebook_v0 ne fonctionne pas pour les tests de ce notebook_v1

def to_percent2(ipynb):
    str = ''
    for c in ipynb['cells']:
        if c['cell_type'] != 'code':
            str += f"# %% [{c['cell_type']}]\n"
        if c['cell_type'] == 'code':
            str += "# %%"
        for l in c['source']:
            if c['cell_type'] == 'code':
                str += f"\n{l}"
            else : 
                str += f"# {l}"
        str += "\n\n"
    str = str[:-2]
    return str

class PyPercentSerializer:
    r"""Prints a given Notebook in py-percent format.

    Args:
        notebook (Notebook): the notebook to print.

    Usage:
            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> ppp = PyPercentSerializer(nb)
            >>> print(ppp.to_py_percent()) # doctest: +NORMALIZE_WHITESPACE
            # %% [markdown]
            # Hello world!
            # ============
            # Print `Hello world!`:
            <BLANKLINE>
            # %%
            print("Hello world!")
            <BLANKLINE>
            # %% [markdown]
            # Goodbye! 👋
    """
    def __init__(self, notebook):
        self.notebook = notebook 

    def to_py_percent(self):
        r"""Converts the notebook to a string in py-percent format.
        """
        return to_percent2(self.notebook.ipynb)


    def to_file(self, filename):
        r"""Serializes the notebook to a file

        Args:
            filename (str): the name of the file to write to.

        Usage:

                >>> nb = Notebook.from_file("samples/hello-world.ipynb")
                >>> s = PyPercentSerializer(nb)
                >>> s.to_file("samples/hello-world-serialized-py-percent.py")
        """
        f = open(filename,'w')
        f.write(self.notebook)
        return f

class Serializer:
    r"""Serializes a Jupyter Notebook to a file.

    Args:
        notebook (Notebook): the notebook to print.

    Usage:

        >>> nb = Notebook.from_file("samples/hello-world.ipynb")
        >>> s = Serializer(nb)
        >>> pprint.pprint(s.serialize())  # doctest: +NORMALIZE_WHITESPACE
            {'cells': [{'cell_type': 'markdown',
                'id': 'a9541506',
                'medatada': {},
                'source': ['Hello world!\n',
                           '============\n',
                           'Print `Hello world!`:']},
               {'cell_type': 'code',
                'execution_count': 1,
                'id': 'b777420a',
                'medatada': {},
                'outputs': [],
                'source': ['print("Hello world!")']},
               {'cell_type': 'markdown',
                'id': 'a23ab5ac',
                'medatada': {},
                'source': ['Goodbye! 👋']}],
            'metadata': {},
            'nbformat': 4,
            'nbformat_minor': 5}
        >>> s.to_file("samples/hello-world-serialized.ipynb")
    """

    def __init__(self, notebook):
        self.notebook = notebook 

    def serialize(self):
        r"""Serializes the notebook to a JSON object

        Returns:
            dict: a dictionary representing the notebook.
        """
        nb = Notebook(self.notebook)
        dict = {}
        dict['cells'] = []
        dict['metadata'] = {}
        version = nb.version.split('.')
        dict['nbformat'] = int(version[0]) #on veut récupérer que le premier chiffre  
        dict['nbformat_minor'] = int(version[1]) 
        for c in nb.cells :
            cell = {}
            cell['metadata'] = {}
            if isinstance(c,MarkdownCell):
                cell['cell_type'] = 'markdown'
                cell['id'] = c.id
                cell['source'] = c.source
            elif isinstance(c, CodeCell):
                cell['cell_type'] = 'code'
                cell['id'] = c.id
                cell['source'] = c.source
                cell['execution_count'] = c.execution_count
            dict['cells'].append(cell)
        return dict 


    def to_file(self, filename):
        r"""Serializes the notebook to a file

        Args:
            filename (str): the name of the file to write to.

        Usage:

                >>> nb = Notebook.from_file("samples/hello-world.ipynb")
                >>> s = Serializer(nb)
                >>> s.to_file("samples/hello-world-serialized.ipynb")
                >>> nb = Notebook.from_file("samples/hello-world-serialized.ipynb")
                >>> for cell in nb:
                ...     print(cell.id)
                a9541506
                b777420a
                a23ab5ac
        """
        f = open(filename,'w')
        f.write(self.serialize)
        return f

class Outliner:
    r"""Quickly outlines the strucure of the notebook in a readable format.

    Args:
        notebook (Notebook): the notebook to outline.

    Usage:

            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> o = Outliner(nb)
            >>> print(o.outline()) # doctest: +NORMALIZE_WHITESPACE
                Jupyter Notebook v4.5
                └─▶ Markdown cell #a9541506
                    ┌  Hello world!
                    │  ============
                    └  Print `Hello world!`:
                └─▶ Code cell #b777420a (1)
                    | print("Hello world!")
                └─▶ Markdown cell #a23ab5ac
                    | Goodbye! 👋
    """
    def __init__(self, notebook):
        self.notebook = notebook

    def outline(self):
        r"""Outlines the notebook in a readable format.

        Returns:
            str: a string representing the outline of the notebook.
        """
        nb = Notebook(self.notebook.ipynb)
        str = f"Jupyter Notebook v{nb.version}\n"
        for cell in nb.cells:
            if isinstance(cell, CodeCell): 
                code = cell
                str += f"└─▶ Code cell #{code.id} ({code.execution_count})\n"
                if len(code.source) == 1: #il n'y a qu'une seule ligne de code à printer
                    str += f"    | {code.source[0]}\n"
                else: #la source de la cellule contient plusieurs lignes de code
                    str += f"    ┌   {code.source[0]}"
                    for source in code.source[1:-1]:
                        str += f"    │ {source}"
                    str += f"    └  {code.source[-1]}\n"
            if isinstance(cell, MarkdownCell): 
                markdown = cell
                str += f"└─▶ Markdown cell #{markdown.id}\n"
                if len(markdown.source) == 1:
                    str += f"    | {markdown.source[0]}\n"
                else:
                    str += f"    ┌  {markdown.source[0]}"
                    for source in markdown.source[1:-1]:
                        str += f"    │  {source}"
                    str += f"    └  {markdown.source[-1]}\n"
        return str[:-1]
