## Grpc Banking System 

This project is a demonstration of a gRPC-based system, simulating a banking system with branches and customers. It uses Python's multiprocessing and concurrent futures to handle multiple clients and servers.

## Files

- `main.py`: This is the main file where the gRPC servers and clients are started.
- `branch_pb2_grpc.py`: This file contains the gRPC stubs and services for the Branch.
- `Branch.py`: This file defines the Branch class, which represents a branch in the banking system.
- `Customer.py`: This file defines the Customer class, which represents a customer in the banking system.

## How it works

The `main.py` file contains two main functions: `serveBranch` and `serveCustomer`.

### serveBranch

This function starts a gRPC server for a branch. It takes a `Branch` object as an argument. The `Branch` object is expected to have an `id` attribute and a `createStubs` method.

The `createStubs` method is called to initialize the gRPC stubs for the branch. Then, a gRPC server is created with a thread pool executor, and the branch is added as a servicer to the server. The server is started on a port that is calculated based on the branch's id, and then it waits for termination.

### serveCustomer

This function starts a gRPC client for a customer. It takes a `Customer` object as an argument. The `Customer` object is expected to have a `createStub` and an `executeEvents` method.

The `createStub` method is called to initialize the gRPC stub for the customer. Then, the `executeEvents` method is called to start the customer's interactions with the branches.

## Inputs and Outputs

The inputs to this system are the `Branch` and `Customer` objects that are passed to the `serveBranch` and `serveCustomer` functions, respectively. These objects should be created and initialized with the necessary data before being passed to these functions.

The outputs of this system are the interactions between the customers and branches, which are handled through gRPC calls. The results of these interactions are not explicitly returned by the `serveBranch` and `serveCustomer` functions, but they can be observed through the gRPC calls that are made.

## How to Run

To run this project, you need to create and initialize `Branch` and `Customer` objects, and then pass them to the `serveBranch` and `serveCustomer` functions in `main.py`. The exact details of how to do this will depend on the specifics of your project setup.



## Quick Start

1. `git clone` the repo and `cd` into the project
2. `python3 -m venv env` to initialize the virtual environment
3. `source env/bin/activate` to activate the virtual environment
4. `pip install -r requirements.txt` to install project dependencies
5. `python main.py input1.json` to start the program
6. The result will be written to `output.txt`

## Overview

### Important Files

The following important files are included in this project:

* `main.py`: Main program to be executed from the command line with: `python main.py input.json`

* `input1.json`: Input file containing a list of branch processes and customer processes with for Monotonic Writes

* `input2.json`: Input file containing a list of branch processes and customer processes with to Read your Writes Cosistency

* `output.txt`: The output file containing each Customer's `recvMsg` output. This file will be overwritten each time the program is ran.

* `branch.proto`: Protocol buffer file defining RPC messages & services. This file has already been compiled to produce the `branch_pb2.py` & `branch_pb2_grpc.py` files.

* `Branch.py`: Branch class served as a gRPC server to process customer transactions and propagate them to other branches.

* `Customer.py`: Customer class with gRPC client branch stub to send transaction requests to its corresponding bank branch.

### Input File

The input file should be in `.json` format and is passed to the program via a command line argument:

```sh
python main.py input.json
```

The following `input.json` file is included from the Project instructions:

```json
[
  {
    "id": 1,
    "type": "customer",
    "events": [
      { "id": 1, "interface": "query", "money": 400 }
    ]
  },
  {
    "id": 2,
    "type": "customer",
    "events": [
      { "id": 2, "interface": "deposit", "money": 170 },
      { "id": 3, "interface": "query", "money": 400 }
    ]
  },
  {
    "id": 3,
    "type": "customer",
    "events": [
      { "id": 4, "interface": "withdraw", "money": 70 },
      { "id": 5, "interface": "query", "money": 400 }
    ]
  },
  {
    "id": 1,
    "type": "branch",
    "balance": 400
  },
  {
    "id": 2,
    "type": "branch",
    "balance": 400
  },
  {
    "id": 3,
    "type": "branch",
    "balance": 400
  }
]

```

### Python Environment

Python 3 is required for this project. `venv` is used to sandbox the Python project and dependencies in a virtual environment.

In order to use the included Python version and project dependency files, the virtual environment must be initialized and activated before the program is ran.

From the project root:

```sh
# Initialize the Python virtual environment
python3 -m venv env

# Activate the virtual environment
source env/bin/activate

# Install project dependencies in the virtual environment
pip install -r requirements.txt
```

For more information, please refer to the [12. Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html) page of the official Python documentation.
