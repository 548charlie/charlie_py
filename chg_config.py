#!/usr/bin/env python

print "Hello world!!!"
import os
import sys


def getopts(args):
    changes = {}
    sites = []
    configs = []
    filename = ""
    option = ""
    for arg in args:
        if (arg.find("-") >= 0 ):
            option = arg
            print "option %s" % option
            continue
        if option == "-s" :
            sites.append(arg)
        elif option == "-c" :
            configs.append(arg)
        elif option == "-f":
            filename = arg
    if len(sites) > 0:
        changes["sites"] = sites
    else :
        print "You have to define at least one site"
        sys.exit(0)
    if len(configs) > 0 :
        changes["configs"] = configs
    else:
        print "You have to define at least one config like NetConfig, Views, Alerts"
        sys.exit(0)
    if filename != "" :
        changes["filename"] = filename
    else:
        print "You have to provide filename with thread names"
        sys.exit(0)
        
    return changes
changes = {}
changes = getopts(sys.argv)
for key in changes.keys():
    print "change %s == %s\n" %(key, changes[key])
sites = changes["sites"]
for site in sites:
    print "change config for %s site\n" % site

