# PerFin
PerFin is a  Personal Finance library for Python

## Features
* Basically a wrapper library for Pandas right now
* Load and handle csv files 
* Calculate montly savings 
* Get the standard deviation of a given account - try to handle the noise :)
* Will add a simple API for backtesting, plotting in Jupyter, monte carlo simulations ... over the next month

## Examples 
To get a PerFin playground execute the following steps

1. Define a environment variable 'PERFIN_FILES' and point it to the directory with the csv files you want to work on
 * on MacOS or Linux it's `export PERFIN_FILES=/home/user/files`. 
 Note: Right now, if you have on folder for all `.csv` files, they will 
 all be put together into one dataframe, regardless if the filenames say 'checking' or 'saving'. 
 
2. Open the interpreter in the `PerFin` folder. Load the playground script from the examples folder. 
 * Option 1: Import the playground module. The code is directly executed and is then available via `playground.data`
 * Option 2: Add the variables to the interpreters global scope e.g. `exec(open("/Users/admin/pythonprojects/perfin/examples/playground.py").read(), globals()`

3. Have fun