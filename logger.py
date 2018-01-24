#!/usr/bin/env python3
"""
Logger library.

Provides a class that allows to log with different levels of relevance
in a specific file, avoinding print statements. The logs have a timestamp
and a label for the particular logger. Logs can be filtered by level,
label or both.

Provides a script to access to the log files created by the Logger class.
Supports optional levels to filter by level (-l) and by label (-L), as well
as the follow option (-f) to see live incoming data.

Created by Eduardo Ponz. 23-01-2018.
"""
import sys
import time

from sys import argv
from datetime import datetime
from time import gmtime, strftime


# *********************** LOGGER CLASS *********************** #
class Logger():
    """
    Class that allows to log with different levels of relevance.

    Logs in the provided file, avoinding print statements.
    The logs have a timestamp and a label for the particular logger.
    Logs can be filtered by level, label or both.
    """

    def __init__(self, file_path, logger_label='logger'):
        """
        Contructor.

        Takes a path for the file to log to. Takes 2 optional arguments,
        a label (which defaults to 'logger'), and days to keep (default 5).
        Logs older than the current date minus days_to_keep will be erased
        for maintance porpuses.

        Calls to __verify_path() and to __clean_old_logs().
        """
        self.file_path = file_path
        self.logger_label = logger_label
        self.__verify_path()
        self.__clean_old_logs()

    def __verify_path(self):
        """Check if the file exists. If it does not, then it creates it."""
        try:
            file = open(self.file_path, "r")
            file.close()
        except FileNotFoundError:
            print("Cannot open the file '" + "'" + self.file_path +
                  ". The file does not exit!")
            print("Creating the file...")
            self.clean_file()
            print("The file '" + self.file_path + "' has been created!")

    def __get_file_lines(self):
        """Return all the lines of the file."""
        lines = 'no file encoutered'
        try:
            file = open(self.file_path, "r")
            lines = file.readlines()
            file.close()
        except FileNotFoundError:
            file = open(self.file_path, "w")
            file.close()
            file = open(self.file_path, "r")
            lines = file.readlines()
            file.close()
        finally:
            return lines

    def __get_last_line_number(self):
        """Return the line number of the last line."""
        lines = self.__get_file_lines()
        line_number = 0
        for line in lines:
            line_number = 0
            for char in line:
                if char is not '-':
                    line_number = line_number * 10 + int(char)
                else:
                    break
        return line_number

    def __clean_old_logs(self):
        """
        Check the timestamp of the entries using days_to_keep.

        If they are to old, it gets rid of them.
        """
        try:
            current_date_string = strftime("%d-%m-%y %H:%M:%S", gmtime())
            current_date = datetime.strptime(current_date_string,
                                             "%d-%m-%y %H:%M:%S")
            lines = self.__get_file_lines()
            if lines != 'no file encoutered':
                file = open(self.file_path, "w")
                for line in lines:
                    seconds = self._get_line_days(line) * 24 * 3600
                    date = ''
                    date_position = False
                    for char in line:
                        if char is '[':
                            date_position = True
                        elif char is ']':
                            break
                        if date_position is True:
                            date += char
                    date_format = datetime.strptime(date[1:],
                                                    "%d-%m-%y %H:%M:%S")
                    if (current_date - date_format).seconds < seconds:
                        file.write(line)
                file.close()
            else:
                raise FileNotFoundError
        except Exception as e:
            raise e

    def _get_line_days(self, line):
        """Return the days_to_remain of line."""
        length = len(line)
        colon_count = 0
        days_to_remain = 0
        for i in range(0, length):
            if line[i] == ':':
                colon_count += 1
            if colon_count is 3:
                i += 1
                days_to_remain = int(line[i])
                while(line[i + 1] is not ']'):
                    i += 1
                    days_to_remain = days_to_remain * 10 + int(line[i])
                break
        return days_to_remain

    def _get_line_level(self, line):
        """Return the log level of line."""
        length = len(line)
        colon_count = 0
        lvl = 0
        for i in range(0, length):
            if line[i] == ':':
                colon_count += 1
            if colon_count is 4:
                i += 1
                lvl = int(line[i])
                while(line[i + 1] is not ']'):
                    i += 1
                    lvl = lvl * 10 + int(line[i])
                break
        return lvl

    def _get_line_label(self, line):
        """Return the log label of line."""
        bracket_count = 0
        label = ''
        for char in line:
            if char is ']':
                bracket_count += 1
            if bracket_count is 3:
                if char is ':':
                    label = label[2:]
                    return label
                else:
                    label += char
        return label

    def log(self, message, level=1, days_to_remain=5):
        """
        Write a log entry specifying the message and the level.

        Format--> line_number-[d-m-y H:M:S][lvl:level] label: message
        """
        if level >= 1:
            time_stamp = strftime("%d-%m-%y %H:%M:%S", gmtime())
            line_number = self.__get_last_line_number() + 1
            file = open(self.file_path, "a")
            file.write(str(line_number) + '-[' + time_stamp + '][d:' +
                       str(days_to_remain) + '][l:' + str(level) + '] ' +
                       self.logger_label + ': ' + message + '\n')
            file.close()
        else:
            raise ValueError('Wrong level value. Level must be bigger than 0')

    def print_level(self, level):
        """Print all the entries with level level."""
        lines = self.__get_file_lines()
        for line in lines:
            lvl = self._get_line_level(line)
            if lvl == level:
                print(line[:-1])

    def print_label(self, label):
        """Print all the entries with level level."""
        lines = self.__get_file_lines()
        for line in lines:
            lbl = self._get_line_label(line)
            if lbl == label:
                print(line[:-1])

    def print_interval(self, interval):
        """
        Print all the entries with level contain in interval.

        Interval is a list of numbers.
        """
        lines = self.__get_file_lines()
        for line in lines:
            lvl = self._get_line_level(line)
            if lvl in interval:
                print(line[:-1])

    def print_interval_by_label(self, interval, label):
        """
        Filter by level and interval.

        Combination of print_level and print_label().
        """
        lines = self.__get_file_lines()
        for line in lines:
            lvl = self._get_line_level(line)
            lbl = self._get_line_label(line)
            if lvl in interval and lbl == label:
                print(line[:-1])

    def print_all(self):
        """Print all entries in the file."""
        lines = self.__get_file_lines()
        if lines:
            for line in lines:
                print(line[:-1])
        else:
            print('The file is empty!')

    def clean_file(self):
        """Delete all the entries in the file."""
        file = open(self.file_path, "w")
        file.close()


# *********************** SCRIPT FUNCTIONS *********************** #
def get_options(argv):
    """Return script optional arguments in a dictionary."""
    options = {}
    while argv:
        try:
            if argv[0][0] == '-' and argv[0][1] != 'f' and argv[0][1] != 'F':
                options[argv[0]] = argv[1]
            argv = argv[1:]
        except:
            print('Incorrect optional argument.' +
                  " Run 'logger -h' for help.")
            sys.exit()
    return options


def validate_options(options):
    """Parse the script option looking for '-l' and '-L'."""
    valid_options = {}
    if '-L' in options:
        valid_options['label'] = options['-L']
    if '-l' in options:
        number = 0
        interval_list = []
        interval_string = options['-l']
        i = 0
        for char in interval_string:
            try:
                i += 1
                if char is not ',':
                    number = number * 10 + int(char)
                else:
                    interval_list.append(number)
                    number = 0
                if char is not ',' and i is len(interval_string):
                    interval_list.append(number)
            except:
                print('Insert a valid interval.' +
                      " Run 'logger -h' for help.")
                sys.exit()
        valid_options['level_int'] = interval_list
    return valid_options


def create_file(file_path):
    """
    Create specify file if it does not exist.

    If the file specify when running the script does not exist,
    the user can choose to create it.
    """
    try:
        file = open(file_path, "r")
        file.close()
        return True
    except FileNotFoundError:
        print("File '" + file_path + "' does not exist.")
        response = input("Do you want to create the file? [y/n]: ")
        while response != 'y' and response != 'n':
            if response != '':
                print("Uninterpretable answer." +
                      " Answer 'y' for yes or 'n' for no.")
            response = input("Do you want to create the file? [y/n]: ")
        if response == 'y':
            print("Creating file...")
            file = open(file_path, "w")
            print("File '" + file_path + "' has been created!")
            file.close()
            return True
        elif response == 'n':
            return False


def print_help():
    """Print the script options."""
    print('Logger options:')
    print('\t-h --Help.')
    print('\t-f --Follow. Prints entries as they come applying ' +
          'the selected optional filters.')
    print('\t-F --Follow. Prints all the file entries and as they ' +
          'come applying the selected optional filters.')
    print('\t-l --Levels. Levels to output level_1,level_2,etc.')
    print('\t-L --Label. Filter by log label')
    print("Example: 'sudo logger $PATH_TO_FILE -l 1,2,3 -L $LOG_LABEL'")


def follow_print(file_path, options):
    """Print entries as they come filter by script options."""
    logger = Logger(file_path)
    file = open(file_path, "r")
    file.seek(0, 2)
    try:
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.02)
            else:
                lvl = logger._get_line_level(line)
                lbl = logger._get_line_label(line)
                if 'label' in options:
                    if options['label'] != lbl:
                        continue
                    pass
                if 'level_int' in options:
                    if lvl not in options['level_int']:
                        continue
                    pass
                print(line[:-1])
    except Exception as e:
        raise e
    finally:
        file.close()


def all_follow_print(file_path, options):
    """Print all file entries and as they come filter by script options."""
    logger = Logger(file_path)
    if 'label' in options:
        if 'level_int' in options:
            logger.print_interval_by_label(options['level_int'],
                                           options['label'])
        else:
            logger.print_label(options['label'])
    elif 'level_int' in options:
        logger.print_interval(options['level_int'])
    else:
        print('The file is empty!')
    file = open(file_path, "r")
    file.seek(0, 2)
    try:
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.02)
            else:
                lvl = logger._get_line_level(line)
                lbl = logger._get_line_label(line)
                if 'label' in options:
                    if options['label'] != lbl:
                        continue
                    pass
                if 'level_int' in options:
                    if lvl not in options['level_int']:
                        continue
                    pass
                print(line[:-1])
    except Exception as e:
        raise e
    finally:
        file.close()

# *********************** SCRIPT BODY *********************** #
if __name__ == '__main__':
    arguments = sys.argv
    if len(arguments) is 1:
        print("Run 'logger -h' for help.")
        sys.exit()
    if len(arguments) is 2:
        if arguments[1] == '-h':
            print_help()
            sys.exit()
        else:
            response = create_file(arguments[1])
            if response is False:
                sys.exit()
            logger = Logger(arguments[1])
            logger.print_all()
            sys.exit()
    if len(arguments) > 2:
        if arguments[1] == '-h':
            print("Cannot run 'logger -h $ARGUMENTS'." +
                  " Run 'logger -h' for help.'")
            sys.exit()
        elif arguments[1] != '-h' and '-h' in arguments:
            print("Cannot run 'logger $ARGUMENTS -h'." +
                  " Run 'logger -h' for help.'")
            sys.exit()
        options = get_options(argv)
        valid_options = validate_options(options)
        if (arguments[1] != '-l' and arguments[1] != '-L' and
                arguments[1] != '-f' and arguments[1] != '-F'):
            response = create_file(arguments[1])
            if response is False:
                sys.exit()
            if '-f' in arguments or '-F' in arguments:
                try:
                    if '-f' in arguments and '-F' not in arguments:
                        follow_print(arguments[1], valid_options)
                    elif '-F' in arguments and '-f' not in arguments:
                        all_follow_print(arguments[1], valid_options)
                    else:
                        print("Incorrect optional argument." +
                              " Cannot use '-f' and '-F' at the same time." +
                              " Run 'logger -h' for help.")
                except:
                    print(' Keyboard Interruption. Closing down...')
                finally:
                    sys.exit()
            else:
                logger = Logger(arguments[1])
                if 'level_int' in valid_options and 'label' in valid_options:
                    logger.print_interval_by_label(valid_options['level_int'],
                                                   valid_options['label'])
                    sys.exit()
                elif 'level_int' in valid_options:
                    logger.print_interval(valid_options['level_int'])
                    sys.exit()
                elif 'label' in valid_options:
                    logger.print_label(valid_options['label'])
                    sys.exit()
                else:
                    print('Incorrect optional argument.' +
                          " Run 'logger -h' for help.")
        else:
            print('First argument should be a file to read.' +
                  " Run 'logger -h' for help.")
