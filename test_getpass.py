#!/usr/bin/env python
import getpass
user_name = raw_input("Enter user name: ")
password = getpass.getpass("Please enter your password: ");

print "You entered %s %s \n"  % (user_name ,password)

