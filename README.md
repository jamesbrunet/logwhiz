# logwhiz
An object oriented python project that processes csv-formatted log data and turns it into something useful for statistical analysis.

## High-Level Explanation
This project is split into three parts:
* The `Main` module
* The `CsvTools` module
* The `User` and `Login` class

Below is an image that shows, in a simplified way, how these modules and classes interact. Green arrows represent function calls, yellow arrows represent file i/o, and orange arrows represent pushing and popping data to and from internal data structures. The number inside the arrow indicates the sequence of the operation.
![The image should be here. If not, imagine something awe-inspiring.](imgs/highlevel_numbers.png?raw=true "Wow, look at that mspaint masterpiece!")

###	The Main Module
This module calls the parser and writer functionality implemented in `CsvTools`. The three csv files are opened and parsed using the CsvTools parse_csv function, while a dictionary of user objects is continuously populated with this data. The contents of the user dictionary are then passed to the `write_csv` function, which dumps this data into a csv file.

###	The CsvTools Module
This module contains functions to write and parse CSV files that contain login data. `parse_csv` updates the user dictionary with the contents of the csv file at the specified path. It handles file i/o, and processes the data by using methods defined within the User and Login objects. `write_csv` sorts the dictionary of users and writes its contents to a csv file at the path specified.

###	The User and Login Classes
The `User` class contains data about a particular user's experience with the system. In particular, their id, whether or not they are currently attempting a login, failed and successful login attempts, and the password scheme which they are using are stored within this class--along with methods that manipulate this data. These methods create login objects, change the active logon attempt, set the status and end time of a login attempt, eliminate logins which are outliers (must be problems with the csv), and formats the data in a way that is friendly to `write_csv`.
	
The `Login` class handles events within the context of a single login. It initializes login events with a start time, calculates the elapsed login time, and parses times (formatted like `2011-07-25 13:09:38`) into datetime objects.
