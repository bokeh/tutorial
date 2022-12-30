# Bokeh tutorial notebooks

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/bokeh/tutorial/main?labpath=notebooks%2F01_introduction.ipynb)

This repository contains a series of Jupyter notebooks.
These notebooks are available as an interactive tutorial at
https://mybinder.org/v2/gh/bokeh/tutorial/main?labpath=notebooks%2F01_introduction.ipynb

To learn about Bokeh, please use the tutorial on [mybinder.org](https://mybinder.org/v2/gh/bokeh/tutorial/main?labpath=notebooks%2F01_introduction.ipynb).

You can also [install and run the notebooks on a local machine](#local-setup).
This is helpful if you can't access mybinder.org, or if you want to
[contribute to this tutorial](#contributing-to-this-tutorial).

## Local setup

To run the tutorial locally, you first need to clone this repository to your local
machine. For example:

```bash
git clone git@github.com:bokeh/tutorial.git
```

After cloning the repository, enter the folder that contains the repository contents:

```bash
cd tutorial
```

Next, you need to set up your environment. This tutorial uses the `conda` package
manager.
Please make sure
[conda or Miniconda are installed and configured correctly](https://docs.conda.io/projects/conda/en/stable/)
on your system.

Run the following command inside your local repository folder to create your environment:

```bash
conda env create -f environment.yml
```

After the environment is set up, activate it with the following command:

```bash
conda activate bk-tutorial
```

From inside this environment, you can now start the Jupyter notebook server:

```bash
jupyter notebook
```

After opening Jupyter notebooks in a browser, go to the folder `notebooks`.
Open the first notebook in this folder. It is called `01_introduction.ipynb`.

## Contributing to this tutorial

Thank you for helping to make this tutorial a better resource for everyone!

Everyone active in the Bokeh project’s codebases, issue trackers, and discussion forums
is expected to follow the
[Code of Conduct](https://github.com/bokeh/bokeh/blob/main/docs/CODE_OF_CONDUCT.md).
This includes working on these tutorials!

Contributing to this tutorial repository works similarly to
[contributing to Bokeh itself](https://docs.bokeh.org/en/latest/docs/dev_guide.html):

1. Open an issue in the [issue tracker of this repository](https://github.com/bokeh/tutorial/issues)
2. Make PR and link it to the issue you created

Once you have created a pull request, a member of the Bokeh core team will begin reviewing your pull request and may request changes or additions. If so, they will help you along the way with any questions you may have.
