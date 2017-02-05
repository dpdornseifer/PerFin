# PerFin
PerFin is a  Personal Finance library for Python

## What is PerFin
It's basically a wrapper library for Pandas and Zipline with the focus on an easy to use interface

### Implemented so far:
* Load and handle csv files 
* Calculate montly savings and outliers  
* Get aggregates for easy analytics
* Support to model simple stock portfolios and doing weight analysis on them.


## How to Install

### Requirements
PerFin, more specific `cvxopt` requires the `umfpack.h` header file. 
On Mac you can easily install it via brew, see the following link: 
[Scientific packages for Python3](https://dedalus-project.readthedocs.io/en/latest/machines/mac_os/mac_os.html#scientific-packages-for-python3)


### More to come 
* Will add a simple API for backtesting, plotting in Jupyter, monte carlo simulations ... over the next month

## Examples
Please have a look at the [examples](https://github.com/dpdornseifer/PerFin/tree/master/examples) directory for all examples.

  
To get a PerFin playground execute the following steps

1. Define a environment variable 'PERFIN_FILES' and point it to the directory with the csv files you want to work on
 * on MacOS or Linux it's 
    ```sh 
    export PERFIN_FILES=/home/user/files
    ```
 * Note: Right now, if you have on folder for all `.csv` files, they will 
  all be put together into one dataframe, regardless if the filenames say 'checking' or 'saving'. 
 
2. Open the interpreter in the `PerFin` folder. Load the playground script from the examples folder. 
 * Option 1: Import the playground module. The code is directly executed and is then available via `playground.data`
 * Option 2: Add the variables to the interpreters global scope e.g. 
   ```python
   exec(open("/Users/admin/pythonprojects/perfin/examples/playground.py").read(), globals())
   ```

3. Have fun
