# Bokeh tutorial notebooks

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/bokeh/tutorial/main?filepath=notebooks%2F01_introduction.ipynb)

This repository contains a series of Jupyter notebooks.
These notebooks are available as an interactive tutorial at
https://mybinder.org/v2/gh/bokeh/tutorial/main?filepath=notebooks%2F01_introduction.ipynb

To learn about Bokeh, please use the tutorial on [mybinder.org](https://mybinder.org/v2/gh/bokeh/tutorial/main?filepath=notebooks%2F01_introduction.ipynb).

You can also [install and run the notebooks on a local machine](#local-setup).
This is helpful if you can't access mybinder.org, or if you want to
[contribute to this tutorial](#contributing-to-this-tutorial).

## Setup for SciPy US 2024

This tutorial will be presented at the SciPy 2024 conference, where you can use Nebari (JupterHub) hosted at [scipy.quansight.dev](https://scipy.quansight.dev/) to follow along.

Follow [this participant's guide](https://docs.google.com/document/d/11YWMZKW6Y4tXnMs3Jekc1S7BQWTR6THZazDaq3WoNxw/edit?usp=sharing) to register, sign-in, and download the tutorial materials.

In the `tutorials/tutorial` folder that's created with all material, navigate to the `notebooks` folder, and open `01_introduction.ipynb`.

The environment for this tutorial is `scipy-scipy-interactive-dataviz-bokeh`, and it is automatically selected for you.

## Previous presentations

### SciPy US 2023

This tutorial was presented live during the SciPy 2023 conference. The state of the repository, as presented, can be accessed through the designated git tag, available [here](https://github.com/bokeh/tutorial/releases/tag/SciPy2023).

Additionally, the tutorial presentation is accessible on YouTube via the following link: https://youtu.be/G0Yc3ck4lC8?si=ZGqatTPnZBwjtdXO

## Local setup

Follow these steps to run the tutorial notebooks on your local machine:

1. To run the tutorial locally, first **clone** this repository to your local machine.
    For example:

    ```bash
    git clone git@github.com:bokeh/tutorial.git
    ```

2. After cloning the repository, **enter the folder** that contains the repository contents:

    ```bash
    cd tutorial
    ```

3. Next, you need to **set up your environment**. This tutorial uses the `conda` package
    manager.
    Please make sure
    [conda or Miniconda are installed and configured correctly](https://docs.conda.io/projects/conda/en/stable/)
    on your system.

    Run the following command inside your local repository folder to create your environment:

    ```bash
    conda env create -f environment.yml
    ```

4. After the environment is set up, **activate** it with the following command:

    ```bash
    conda activate bk-tutorial
    ```

5. Before opening the tutorial notebooks, you need to **install the Bokeh sampledata**.
    Make sure the ``bk-tutorial`` environment is activated, then run the following command:

    ```bash
    bokeh sampledata
    ```

6. From inside the  ``bk-tutorial`` environment, you can now **start the Jupyter
    notebook server**:

    ```bash
    jupyter notebook
    ```

7. After opening Jupyter notebooks in a browser, go to the folder `notebooks`.
    **Open the first notebook in this folder**. It is called
    `01_introduction.ipynb`.

## Contributing to this tutorial

Thank you for helping to make this tutorial a better resource for everyone!

Everyone active in the Bokeh project’s codebases, issue trackers, and discussion forums
is expected to follow the
[Code of Conduct](https://github.com/bokeh/bokeh/blob/main/docs/CODE_OF_CONDUCT.md).
This includes working on these tutorials!

### Preparing your environment

The ``bk-tutorial`` environment includes the necessary dependencies to contribute to this repository.

For consistency, we ask that you generally follow the
[Black code style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)
wherever possible.

### Making changes

Contributing to this tutorial repository works similarly to
[contributing to Bokeh itself](https://docs.bokeh.org/en/latest/docs/dev_guide.html):

1. Open an issue in the [issue tracker of this repository](https://github.com/bokeh/tutorial/issues)
2. Make PR and link it to the issue you created

Once you have created a pull request, a member of the Bokeh core team will begin reviewing your pull request and may request changes or additions. If so, they will help you along the way with any questions you may have.
