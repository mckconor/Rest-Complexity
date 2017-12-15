# Rest Service Development Task

### Ignore Master/Slave architecture, not enough time given to complete. Manager/Worker fully implemented.

To run, open multiple cmd or powershell windows use the following commands:

-python .\manager.py

-python .\worker.py

The manager compiles a list of work to be done across files and commits on a git repo. This implementation only computes Cyclomatic Complexity of .py files.
The manager delegates unnassigned work to each worker.py that is spun up.

## New!
-Added results to manager screen when complete:

workStartedAt:  1513377685.5650442

workFinishedAt:  1513377699.3102243

Number of workers:  3

Time to compute:  13.745180130004883

Average Cyclomatic Complexity:  0.8849673202614382


## To-do (if had more time)
-Reallocate work if worker times out on file
