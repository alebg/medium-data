# Medium Data

This repository contains a collection of utilities for processing and analyzing medium-sized datasets.


# Setup

To set up the environment, you can use the following command:

```bash
python -m venv .venv
source .venv/bin/activate

pip install -e .
```

# Usage

You can use the utilities provided in this repository to process and analyze datasets. The main functionalities are encapsulated in the `medium_data` module.


# Example

```bash
python -m medium_data.utils.csv_to_parquet -c "/home/alebg/Descargas/test.csv" -p "data/test.parquet"
```