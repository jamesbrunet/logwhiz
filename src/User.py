# -*- coding: utf-8 -*-
"""Contains only the User class."""

from Login import Login
from collections import OrderedDict
import statistics


class User:

    """Contains data about a particular user's experience with the system.
     
    In particular, their id, whether or not they are currently attempting a login, failed and successful login 
    attempts, and the password scheme which they are using are stored within this class--along with methods that
    manipulate this data.
        
    """

    def __init__(self, uid):
        """Creates a user with zero login attempts and no password scheme."""
        self.user_id = uid
        self.active_login_attempt = None
        self.login_success_list = []
        self.login_failure_list = []
        self.password_scheme = ''

    def create_login(self, start, ps):
        """Creates a login object and sets it as the active login attempt.
        
        If a login attempt is created before the current active login attempt has finished, the current active
        login attempt is overwritten. It is assumed that the user accidentally closed the window.
            
        It is also assumed that an individual user will always have the same password scheme.
            
        """
        self.active_login_attempt = Login(start)
        self.password_scheme = ps

    def finish_login(self, end, status):
        """Completes the active login attempt.

        The active login attempt is given an end time and a status, and then is appended to either the success list
        or failure list depending on this status. The active login attempt is then cleared.
        
        """
        if status == "failure":
            self.active_login_attempt.complete_login(end, False)
            self.login_failure_list.append(self.active_login_attempt)
        elif status == "success":
            self.active_login_attempt.complete_login(end, True)
            self.login_success_list.append(self.active_login_attempt)
        else:
            raise ValueError(status + " is not a valid login status (success or failure)")

        self.active_login_attempt = None


    @staticmethod
    def filter_login_list_outliers(login_list):
        """Filters outliers and returns a list of times in seconds instead of timedeltas.
        
        Some login times are ridiculous: caused by errors in the system. Any login which takes more
        than 60 seconds is unreasonable. I came to this number by inspecting the mean, median, and std
        deviation of the dataset.
        
        """
        login_list = [login.elapsed_time.total_seconds() for login in login_list]
        for i, time in (enumerate(login_list)):
            if time > 60:
                del login_list[i]
        return login_list

    def get_data_required_for_csv(self):
        """Returns an ordered dictionary which is used to generate this user's entry in the csv."""
        success_list_filtered = self.filter_login_list_outliers(self.login_success_list)
        failure_list_filtered = self.filter_login_list_outliers(self.login_failure_list)

        successful_logins = len(success_list_filtered)
        failed_logins = (len(failure_list_filtered))
        num_logins = successful_logins + failed_logins

        mean_success_time, median_success_time, stdev_success_time = None, None, None
        if successful_logins:
            # In this case we can calculate the mean and median
            mean_success_time = statistics.mean(success_list_filtered)
            median_success_time = statistics.median(success_list_filtered)
        if successful_logins > 1:
            # In this case we can calculate the standard deviation
            stdev_success_time = statistics.stdev(success_list_filtered)

        mean_failure_time, median_failure_time, stdev_failure_time = None, None, None
        if failed_logins:
            # In this case we can calculate the mean and median
            mean_failure_time = statistics.mean(failure_list_filtered)
            median_failure_time = statistics.median(failure_list_filtered)
        if failed_logins > 1:
            # In this case we can calculate the standard deviation
            stdev_failure_time = statistics.stdev(failure_list_filtered)

        return OrderedDict([
            ("User ID", self.user_id),
            ("Scheme", self.password_scheme),
            ("Login Attempts", num_logins),

            ("Success Count", successful_logins),
            ("Average Success Time", mean_success_time),
            ("Median Success Time", median_success_time),
            ("Success Time Std Deviation", stdev_success_time),

            ("Fail Count", failed_logins),
            ("Average Failure Time", mean_failure_time),
            ("Median Failure Time", median_failure_time),
            ("Failure Time Std Deviation", stdev_failure_time)
            ])


    def __str__(self):
        """For debugging use only: returns a formatted string containing all data in the object."""
        return("USER ID: " + self.user_id + "\n" +
               "PASSWORD SCHEME: " + self.password_scheme + "\n" +
               "ACTIVE LOGIN: " + str(self.active_login_attempt) + "\n" +
               "SUCCESSFUL LOGINS: " + ", ".join(str(login) for login in self.login_success_list) + "\n" +
               "FAILED LOGINS: " + ", ".join(str(login) for login in self.login_failure_list) + "\n")
