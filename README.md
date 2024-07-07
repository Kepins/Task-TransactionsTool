# Task-TransactionsTool

## Overview

This project consists of a small library designed for reading and writing files in a fixed-width format. It also includes a command-line interface (CLI) application that allows users to interact with these files. The application supports operations such as retrieving the value of any field, modifying field values, and adding transactions.

## Requirements

- Python 3.11
- Additional requirements are listed in the `requirements.txt` file.

## Installation

1. Create a virtual environment (optional but recommended):

    ```sh
    python3.11 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

To get help on how to use the script, run:

```sh
python main.py --help
```

### Examples
To retrieve the value of the "name" field from a file named transactions.trans, use the following command:
```sh
python main.py transactions.trans get name
```

To set the value of the "name" field in a file named transactions.trans, use the following command:
```sh
python main.py transactions.trans set name "NEW NAME"
```

To add transaction to a file named transactions.trans, use the following command:
```sh
python main.py transactions.trans add transaction 1000 PLN
```

## Tests

To run tests use

```sh
pytest .
```