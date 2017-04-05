# -*- coding: utf-8 -*-
"""Contains functions to write and parse CSV files that represent login data."""
import csv
from operator import attrgetter
from User import User


def parse_csv(user_dict, csv_path):
    """Updates user dictionary based off the contents of the csv file.
        
    Note that user_dict may be empty, and csv_path must be valid. 
        
    Arguments:
    user_dict -- dictionary of user names mapped to user objects. This is an input and output parameter.
    csv_path -- partial path of csv file: root dir is the project directory. This is an input parameter.
        
    """
    # Helpful variables to work with csv columns
    time_col = 0
    site_col = 1  # Note: Unused
    user_col = 2
    scheme_col = 3
    mode_col = 4
    event_col = 5
    data_col = 6  # Note: Unused

    with open(csv_path, 'r') as csv_file:
        next(csv_file)  # Skip first line
        log_reader = csv.reader(csv_file, dialect="excel")
        for log in log_reader:
            current_user = log[user_col]

            if current_user in user_dict:
                if log[mode_col] == "enter" and log[event_col] == "start":
                    user_dict[current_user].create_login(log[time_col], log[scheme_col])

                if log[mode_col] == "login" and user_dict[current_user].active_login_attempt:
                    user_dict[current_user].finish_login(log[time_col], log[event_col])
            else:
                user_dict[current_user] = User(current_user)  # Create new user


def write_csv(path, user_dict):
    """Writes the contents of the user dictionary to a csv file at path specified.

    Note that the path must be valid

    Arguments:
    path -- desired path of csv file: root dir is the project directory. This is an input parameter.
    user_dict -- dictionary of user names mapped to user objects. This is an input parameter.

    """
    # Convert user_dict to a list sorted by userid
    users = sorted(list(user_dict.values()), key=attrgetter("user_id"))

    with open(path, 'w') as csv_file:
        csv_writer = csv.writer(csv_file, dialect='excel', lineterminator='\n')

        # Write the first row of the csv file. Note that users[0] is accessed only to get the keys of the dict
        csv_writer.writerow(list(users[0].get_data_required_for_csv().keys()))

        # Write the remaining rows
        for user in users:
            print(list(user.get_data_required_for_csv().values()))
            csv_writer.writerow(list(user.get_data_required_for_csv().values()))
