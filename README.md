# Rest Service Development Task

### Ignore Master/Slave architecture, not enough time given to complete. Manager/Worker fully implemented.

To run, open multiple cmd or powershell windows use the following commands:

-python .\manager.py

-python .\worker.py

The manager compiles a list of work to be done across files and commits on a git repo. This implementation only computes Cyclomatic Complexity of .py files.
The manager delegates unnassigned work to each worker.py that is spun up.

## To-do
-Reallocate work if worker times out on file

-Add means of tracking "Time to completion" to compare different number of worker nodes
