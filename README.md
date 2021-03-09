# Robo Advisor

A Python application that allows the user to analyze recent information about chosen stocks.  Additionally, the program provides a buy or sell recommendation.

## Prerequisites

  + Anaconda 3.7+
  + Python 3.7+
  + Pip

## Installation

Fork this [remote repository](https://github.com/mcoyne16/robo-advisor) under your own control, then "clone" or download your remote copy onto your local computer.

Then navigate there from the command line (subsequent commands assume you are running them from the local repository's root directory):

```sh
cd ~/Desktop/robo-advisor
```

Use Anaconda to create and activate a new virtual environment, perhaps called "stocks-env":

```sh
conda create -n stocks-env python=3.8 # (first time only)
conda activate stocks-env
```

From inside the virtual environment, install package dependencies:

```sh
pip install -r requirements.txt
```

> NOTE: if this command throws an error like "Could not open requirements file: [Errno 2] No such file or directory", make sure you are running it from the repository's root directory, where the requirements.txt file exists (see the initial `cd` step above)

## Setup

In in the root directory of your local repository, create a new file called ".env", and update the contents of the ".env" file to include ur API key:

    ALPHAVANTAGE_API_KEY="abc123"

## Usage

Run the program:

```py
python app/robo_advisor.py

```

The user will be prompted to enter stock symbols or tickers one at a time. The user should type 'DONE' when finished. Further, the user will be prompted with a y/n to elect to see a line chart if they so choose.