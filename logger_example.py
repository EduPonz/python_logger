"""
Script example for implementation of Logger class.

Created by Eduardo Ponz. 23-01-2018.
"""
import os

from logger import Logger


if __name__ == '__main__':
    file_path = os.path.dirname(__file__)
    file_path = os.path.abspath(os.path.join(file_path, "log.log"))
    logger_1 = Logger(file_path, 'logger_example_1', days_to_keep=8)
    logger_2 = Logger(file_path, 'logger_example_2', days_to_keep=8)

    # logger_1.clean_file()

    for i in range(1, 16):
        logger_1.log('This is a log!', i)
        logger_2.log('This is a log!', i)

    print('\n----- PRINT ALL ENTRIES WITH LEVEL 1 -----')
    logger_1.print_level(1)

    print("\n----- PRINT ALL ENTRIES WITH LABEL 'logger_example_2' -----")
    logger_1.print_label('logger_example_2')

    print('\n----- PRINT ALL ENTRIES WITH LEVEL 1, 3 or 8 -----')
    logger_1.print_interval([1, 3, 8])

    print('\n----- PRINT ALL ENTRIES WITH LEVEL 1, 3 or 8 ' +
          "AND LABEL 'logger_example_2' -----")
    logger_1.print_interval_by_label([1, 3, 8], 'logger_example_2')

    print('\n----- PRINT ALL ENTRIES -----')
    logger_1.print_all()
