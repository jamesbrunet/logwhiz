# -*- coding: utf-8 -*-
"""Contains only the Login class."""
from datetime import datetime


class Login:

    """Handle events within single login."""

    def __init__(self, start):
        """Creates an 'incomplete' login with the start time specified."""
        self.start_time = Login.parse_time(start)
        self.end_time = None
        self.elapsed_time = None
        self.success = None

    def complete_login(self, end_t, s):
        """Takes an end time and a status boolean (True for success, False for failure) and calculates time elapsed."""
        self.end_time = Login.parse_time(end_t)
        self.elapsed_time = self.end_time - self.start_time
        self.success = s

    @staticmethod
    def parse_time(ts):
        """Converts a string representation of a date (formatted like 2011-07-25 13:09:38) into a datetime object."""
        return datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')

    def __str__(self):
        """For debugging use only: returns a formatted string containing all data in the object."""
        return("Start: " + str(self.start_time) + ", End: " + str(self.end_time) +
               ", Elapsed : " + str(self.elapsed_time) + ", Success: " + str(self.success))
