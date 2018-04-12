# README #

Thank you for your reviewing my entry! This README will guide the grader in successfully running my contribution. 

### This Repository is for Sam Taimourzadeh's Insight EDGAR-analytics Coding Challenge Submission ###

1. For this challenge, I use: 
    * Python 3.4.5 :: Anaconda 4.3.1 (x86_64)
    * Numpy 1.11.3
    * Pandas 0.19.2
2. Data is manipulated via use of Pandas' DataFrames.
3. Multi-threading can be added to speed up processing of weblog sessions, but it is not implemented here. 


### Setup ###

1. Program: `src/edgar-analytics.py`
    * usage: python [path_to_program] --data [input_data_file_path] --inactivity_period [inactivity_period_data_file_path] --output [output_file_path]
        * path_to_program : path to edgar-analytics.py.
        * input_data_file_path : path to EDGAR weblog input file: `log.csv`. Default: `./input/log.csv`
        * inactivity_period_data_file_path: path to inactivity period file: `inactivity_period.txt`. Default: `./input/inactivity_period.txt`
        * output_file_path: path to output file: `sessionization.txt`. Default: `./output/sessionization.txt`


2. How to run pre-passed tests:
    * 4 new tests have been run in `insight_testsuite/tests` 
    * validation of tests can be preformed in `insight_testsuite/` via: 
        `insight_testsuite~$ ./run_tests.sh` 


3. How to run new tests from test folders:
    * New tests can be performed in `insight_testsuite/tests/[new directory]`
    * to validate new tests with `run_tests.sh`, as above, create:
        * `insight_testsuite/tests/[new directory]/input`
            * the desired `log.csv` and `inactivity_period.txt` can be placed here (to use defaults).
        * `insight_testsuite/tests/[new directory]/output`
    * and from `insight_testsuite/tests/[new directory]`, run: `python [path_to_program]`
        * this will use the default (for simplicity) input and output file paths to run.
