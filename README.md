# python_logger
`logger.py` provides a `Logger` python class to log messages with different debugging level. The logs include a line number, a timestamp (d-m-y H:M:S), a number or days to be kept, a level, and a label. It is possible to set the amount of days that the message should be kept in the file before it is deleted (the default value is 5 days). `logger.py` it is also a ptyhon script to read `Logger` class messages and present them on terminal. It supports filters for levels and labels, as well as the options to see the messages as they arrive.

## `Logger` Class
The `Logger` class provides a `log` method to create file entries and several methods to filter them according to different parameters:
  - **`Constructor`** --> Takes the path to the file where the logs should be stored as a mandatory argument, a label as an optional arguments (default is `logger`), and number of days to keep the logs (default is 5). Logs older than the `days_to_keep` value would be deleted.
  - **`log`** --> Takes a message, a debugging level, and the number of days to keep the log as arguments, and creates the log in the file.
  - **`print_level`** --> Takes a level and prints all the messages that correspond to that level.
  - **`print_label`** --> Takes a label and prints all the messages that correspond to that label.
  - **`print_interval`** --> Takes a list of levels and prints all the messages that correspond to those levels.
  - **`print_interval_by_label`** --> Takes an interval of levels and a label and prints all the messages that correspond to those levels and have the supplied label.
  - **`print_all`** --> Prints all the messages present in the file.
  - **`clean_file`** --> Deletes all the messages in the file.
### Log example
```sh
1-[23-01-18 15:20:00][d:2][l:1] logger_example_1: This is a log!
```
#### `logger_example.py`
`logger_example.py` is a python script that serves as a example of implementation for the `Logger` class. It creates 2 `Logger` objects with different labels and creates 15 logs for each of them in a file called `log.log` located in the `logger_example.py` directory. Then it implements all the public methods of the `Logger` class to show their functionalities.


## Logger script
The `logger` script is a terminal tool to retrieve information of logging files created with the `Logger` class. It takes several different arguments:

  - **File path (mandatory)** --> It can be an absolute path or a relative path from the current directory.
  - **-h (optional)** --> Help. Displays the logger options. It has to be used without a file path.
  - **-f (optional)** --> Follow. Prints entries as they come applying the selected optional filters (if present).
  - **-F (optional)** --> Follow. Print all the file entries with the selected optional filters + the ones that come and fulfil the filter requirements.
  - **-l (optional)** --> Levels. It is a list of comma separated level number to filter the logs by debugging level.
  - **-L (optional)** --> Label. Filter the logs by label.

### Installation
The `logger` script can be run as a normal python script (optional arguments have to be passed after $PATH_TO_FILE and can appear in every order):
```sh
$ sudo python3 $PATH_TO_SCRIPT_DIR/logger.py -h
$ sudo python3 $PATH_TO_SCRIPT_DIR/logger.py $PATH_TO_FILE
$ sudo python3 $PATH_TO_SCRIPT_DIR/logger.py $PATH_TO_FILE -f
$ sudo python3 $PATH_TO_SCRIPT_DIR/logger.py $PATH_TO_FILE -F
$ sudo python3 $PATH_TO_SCRIPT_DIR/logger.py $PATH_TO_FILE -l 1
$ sudo python3 $PATH_TO_SCRIPT_DIR/logger.py $PATH_TO_FILE -l 1,2,3
$ sudo python3 $PATH_TO_SCRIPT_DIR/logger.py $PATH_TO_FILE -L $LOG_LABEL
$ sudo python3 $PATH_TO_SCRIPT_DIR/logger.py $PATH_TO_FILE -l 1,2,3 -L $LOG_LABEL
$ sudo python3 $PATH_TO_SCRIPT_DIR/logger.py $PATH_TO_FILE -l 1,2,3 -L $LOG_LABEL -f
$ sudo python3 $PATH_TO_SCRIPT_DIR/logger.py $PATH_TO_FILE -l 1,2,3 -L $LOG_LABEL -F
```
Furhtermore, it can be run as a terminal executable with a short installation proccess:
```sh
$ sudo chmod +x $PATH_TO_SCRIPT_DIR/logger.py
$ sudo cp $PATH_TO_SCRIPT_DIR/logger.py /usr/bin/logger
```
After that, it can be run as a terminal executable:
```sh
$ sudo logger -h
$ sudo logger $PATH_TO_FILE
$ sudo logger $PATH_TO_FILE -f
$ sudo logger $PATH_TO_FILE -F
$ sudo logger $PATH_TO_FILE -l 1
$ sudo logger $PATH_TO_FILE -l 1,2,3
$ sudo logger $PATH_TO_FILE -L $LOG_LABEL
$ sudo logger $PATH_TO_FILE -l 1,2,3 -L $LOG_LABEL
$ sudo logger $PATH_TO_FILE -l 1,2,3 -L $LOG_LABEL -f
$ sudo logger $PATH_TO_FILE -l 1,2,3 -L $LOG_LABEL -F
```
