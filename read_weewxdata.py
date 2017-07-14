#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  NAME: read_weewxdata.py

  PURPOSE:
    To read in data from a weewx.sdb file and plot selected variables.

  CALLS:
    - Python (known to work on Python version 2.7.11)
    - Matplotlib (known to work on Matplotlib version 1.5.1)
    - Built-in Python modules cycler, numpy, math, time, sqlite3, and sys

  MODIFICATIONS:
    - Andrea Neumann <andrea.neumann2@gmail.com> 10 July 2017: Written
    - Andrea Neumann <andrea.neumann2@gmail.com> 12 July 2017: Debugged, added 
        command-line keyword input, removed hard-coded example code, and added
        a bar graph option for the rain4day variable.  Also started on creating
        module header information and documentation.
    - Andrea Neumann <andrea.neumann2@gmail.com> 13 July 2017: Added much of the
        module header information, started working on adding plotting on a second
        y-axis capability, and added another color cycle for the second y-axis 
        variables. Moved the second y-axis variable(s) legend to the top of the 
        figure and set a whitespace padding around the figure in order for the 
        legend to show if there are second y-axis variables present.
    - Andrea Neumann <andrea.neumann2@gmail.com> 14 July 2017: Added notes on
        which version of Python and Matplotlib this module was developed and
        tested on.

  USAGE:
    [python] read_weewxdata.py inputfile=inputfile start=date/time1 end=date/time2 plot_var="var1","var2",...,"varn" [--verbose] [--view_request_time] [debug=0|1] [verbose=0|1] [plot_var2="var1","var2",...,"varn"] 
    - Optional parameters are listed within square brackets ([]).

  EXAMPLE:
    - To plot minimum windchill, heat index, dewpoint, and outside temperature data
      from 2 July 2017 at 19:00:00 CDT to 5 July 2017 at 19:00:00 CDT:
        read_weewxdata.py inputfile='weewx.sdb' start='2017-07-02T19:00:00' end='2017-07-05T19:00:00' plot_var="MinWindChill","HeatIndex","Dewpoint","OutTemp"
    - To plot the outside temperature on the left-hand plot axis and the cumulative 
      rainfall, the rainfall accumulated in one minute, and the rainfall rate on the
      right-hand plot axis from 3 July 2017 at 19:00:00 to 13 July 2017 at 06:00:00
      CDT with verbose command-line output:
        python read_weewxdata.py inputfile='weewx.sdb' start='2017-07-03T19:00:00' end='2017-07-13T06:00:00' plot_var="OutTemp" --verbose plot_var2="CumulativeRain","Rainfall","RainRate"

  INPUT:
    Required keywords:
      inputfile ......... The name of the input file (usually going to be weewx.sdb)
      start ............. The date and time of the starting point; must be in the 
                            format [Year]-[month]-[day]T[hour]:[minute]:[second]
                            Example: 2017-07-09T19:53:05  -where the date is 9th of 
                            July 2017 at 7:53:05 pm". 
                            Can also be called 'archive_time1' or 'start_time'.
      end ............... The date and time of the ending point; must be in the 
                            format [Year]-[month]-[day]T[hour]:[minute]:[second]
                            Example: 2017-07-10T20:04:06  -where the date is 10th of 
                            July 2017 at 8:04:06 pm".
                            Can also be called 'archive_time2' or 'end_time'
      plot_var .......... A list, comma delimited, of variable names in quotation 
                            marks.  Note: There cannot be any spaces either between 
                            variables or within variable names.
    Optional keywords:
      debug ............. Turns on extra command line output for debugging purposes.
                            Same as 'verbose'.
      -h ................ Sends a short helpful message to the command line.
      --help ............ Sends a short helpful message to the command line.
      gmt_offset ........ The offset of the current (or desired) timezone from 
                            GMT/UTC in fraction of a day.  Example: gmt_offset=0.25 
                            offsets the time by a quarter of a day (6 hours).
      plot_var2 ......... A list, comma delimited, of variable names in quotation 
                            marks that will be plotted on a second y-axis.  
                            Note: There cannot be any spaces either between 
                            variables or within variable names.
      -sh ............... Sends a short helpful message to the command line.  Same
                            as '-h'.
      -short-help ....... Sends a short helpful message to the command line.  Same
                            as '-h'.
      -v ................ Turns on extra command line output.
      --verbose ......... Turns on extra command line output.
      verbose ........... Value of one (1) turns on extra command line output.
      view_request_time . A value of one (1) forces the graph to plot in the 
                            date/time range given in the start and end keywords 
                            regardless of data availability.
      --view_request_time . Same as 'view_request_time=1'
      
  OUTPUT:
    A graphic in a pop-up gui.

  POSSIBLE PLOTTING VARIABLES:
    Raw Data Variables (those provided in the inputfile and at full time frequency)
      'Epochtime', 'USUnits',  'SampleInterval', 'Barometer',   'Pressure',  
      'Altimeter', 'InTemp',   'OutTemp',        'InHumidity',  'OutHumidity', 
      'WindSpeed', 'WindDir',  'WindGust',       'WindGustDir', 'RainRate', 
      'Rainfall',  'Dewpoint', 'WindChill',      'HeatIndex',   'Unknown1', 
      'Empty1',    'Empty2',   'Empty3',         'Empty4',      'Empty5', 
      'Empty6',    'Empty7',   'Empty8',         'Empty9',      'Empty10', 
      'Empty11',   'Empty12',  'Empty13',        'Empty14',     'Empty15', 
      'Empty16',   'Empty17',  'Empty18',        'Empty19',     'SignalQuality', 
      'Unknown2',  'Unknown3', 'Empty20',        'Empty21',     'Empty22', 
      'Empty23',   'Empty24',  'Empty25',        'Empty26',     'Empty27', 
      'Empty28',   'Empty29'

    Derived Data Variables at full time frequency (Variables that are derived in
    this module and have the same time frequency as the input data.
      'ADdays', 'CumulativeRain'

    Derived Data Variables at once-daily frequency
      'ADDailyDate', 
      'MaxEpochtime',      'MinEpochtime',      'MaxUSUnits',     'MinUSUnits',
      'MaxSampleInterval', 'MinSampleInterval', 'MaxBarometer',   'MinBarometer',
      'MaxPressure',       'MinPressure',       'MaxAltimeter',   'MinAltimeter',
      'MaxInTemp',         'MinInTemp',         'MaxOutTemp',     'MinOutTemp', 
      'MaxInHumidity',     'MinInHumidity',     'MaxOutHumidity', 'MinOutHumidity',
      'MaxWindSpeed',      'MinWindSpeed',      'MaxWindDir',     'MinWindDir',
      'MaxWindGust',       'MinWindGust',       'MaxWindGustDir', 'MinWindGustDir',
      'MaxRainRate',       'MinRainRate',       'MaxRainfall',    'MinRainfall',
      'MaxDewpoint',       'MinDewpoint',       'MaxWindChill',   'MinWindChill',
      'MaxHeatIndex',      'MinHeatIndex',    'MaxSignalQuality', 'MinSignalQuality',

      'MaxEmpty1',         'MinEmpty1',         'MaxEmpty2',      'MinEmpty2', 
      'MaxEmpty3',         'MinEmpty3',         'MaxEmpty4',      'MinEmpty4', 
      'MaxEmpty5',         'MinEmpty5',         'MaxEmpty6',      'MinEmpty6',
      'MaxEmpty7',         'MinEmpty7',         'MaxEmpty8',      'MinEmpty8',
      'MaxEmpty9',         'MinEmpty9',         'MaxEmpty10',     'MinEmpty10',
      'MaxEmpty11',        'MinEmpty11',        'MaxEmpty12',     'MinEmpty12',
      'MaxEmpty13',        'MinEmpty13',        'MaxEmpty14',     'MinEmpty14',
      'MaxEmpty15',        'MinEmpty15',        'MaxEmpty16',     'MinEmpty16',
      'MaxEmpty17',        'MinEmpty17',        'MaxEmpty18',     'MinEmpty18',
      'MaxEmpty19',        'MinEmpty19',        'MaxEmpty20',     'MinEmpty20',
      'MaxEmpty21',        'MinEmpty21',        'MaxEmpty22',     'MinEmpty22',
      'MaxEmpty23',        'MinEmpty23',        'MaxEmpty24',     'MinEmpty24',
      'MaxEmpty25',        'MinEmpty25',        'MaxEmpty26',     'MinEmpty26',
      'MaxEmpty27',        'MinEmpty27',        'MaxEmpty28',     'MinEmpty28',
      'MaxEmpty29',        'MinEmpty29',        'MaxUnknown1',    'MinUnknown1',
      'MaxUnknown2',       'MinUnknown2',       'MaxUnknown3',    'MinUnknown3', 
      'Rain4Day'

  NOTES:
    - This module was developed and successfully tested on Python 2.7.11 and Matplotlib 1.5.1
    - Made use of online sample code from http://zetcode.com/db/sqlitepythontutorial/ 
      and https://groups.google.com/forum/#!msg/weewx-user/Plw2MjoV8NY/wz1XH45XDwAJ
    - Weather Data order help came from: http://sospilot.readthedocs.io/en/latest/weatherstation.html
    - https://docs.python.org/2/library/time.html was a very helpful website for the
      time conversion code.
    - Code for setting a default matplotlib color cycle came from:
       https://matplotlib.org/examples/color/color_cycle_demo.html and 
       https://matplotlib.org/users/dflt_style_changes.html#colors-in-default-property-cycle

"""
#-----------------------------------------------------------------------------------
# Import python modules
#-----------------------------------------------------------------------------------
import sys
import time
import math
import matplotlib as mpl
import numpy as np
import sqlite3 as lite  # (Should be) built-in module for reading *.sdb files
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from cycler import cycler

#-----------------------------------------------------------------------------------
# Custom classes, functions, modules, etc.
#-----------------------------------------------------------------------------------
def convert_localtime2epochtime(timestring):
  """
    NAME: Convert_time() function
    PURPOSE: To take a given time string and convert it from local time to seconds
             from the start of the epoch UTC.  If input string is incorrectly 
             formatted, then an error is produced and the module closes.
    INPUT:  A string giving a time in the format: Year-month-dayThour:minute:second
    RETURNS: Time in seconds from the start of the epoch UTC
  """
  try:
    epochtime = time.mktime(time.strptime(timestring, '%Y-%m-%dT%H:%M:%S'))
    return epochtime
  except:
    print "ERROR: Time is incorrectly formatted."
    print "       Correct format is: Year-month-dayThour:minute:second"
    print "       Example: 2017-07-09T19:53:05  -where the date is 9th of July 2017 at 7:53:05 pm"
    exit()

#-----------------------------------------------------------------------------------
def short_help_message():
  """
    NAME: long_help_message() function
    PURPOSE: To give a more detailed explanation of how to use this module, including
             the names of all variables available for plotting.
    INPUT: None
    RETURNS: Nothing
  """
  print "\nNAME:    read_weewxdata.py"
  print "PURPOSE: To read in data from a weewx.sdb file and plot selected variables."
  print "USAGE:   [python] read_weewxdata.py inputfile=inputfile start=date/time1 end=date/time2 plot_var='var1','var2',...,'varn' [--verbose] [--view_request_time] [debug=0|1] [verbose=0|1] [plot_var2='var1','var2',...,'varn'] "
  print " - Optional parameters are listed within square brackets ([])."
  print "EXAMPLE: read_weewxdata.py inputfile='weewx.sdb' start='2017-07-02T19:00:00' end='2017-07-05T19:00:00' plot_var='MinWindChill','HeatIndex','Dewpoint','OutTemp'"
  print " - To plot minimum windchill, heat index, dewpoint, and outside temperature data from 2 July 2017 at 19:00:00 CDT to 5 July 2017 at 19:00:00 CDT"
  print "INPUT:"
  print "  Required keywords: inputfile, start, end, plot_var"
  print "  Optional keywords: debug, -h, --help, gmt_offset, plot_var2, -sh, -short-help, -v, --verbose, verbose, view_request_time, --view_request_time"
  print "OUTPUT:  A graphic in a pop-up gui."
  print "\nSee either README.md or read_weewxdata.py header for more information."

#-----------------------------------------------------------------------------------
# Main Module
#-----------------------------------------------------------------------------------
sstarttime = time.time()

# Set up default versions of input keywords
archive_time1 = ''
archive_time2 = ''
gmt_offset    = 0.25  # Calculate the day starting at 06 UTC (00 CST or 01 CDT)
inputfile     = ''
plot_var      = []
plot_var2     = []
verbose       = 0
view_request_time = 0

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Grab keyword input from the command line
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if (len(sys.argv) > 1):
  for item in sys.argv:
    line1 = item.split('=')
    # Required keywords
    if (line1[0] == 'inputfile'):
      inputfile=line1[1]
    elif ((line1[0] == 'archive_time1') or (line1[0] == 'start_time') or 
          (line1[0] == 'start')):
      archive_time1=line1[1]
    elif ((line1[0] == 'archive_time2') or (line1[0] == 'end_time') or 
          (line1[0] == 'end')):
      archive_time2=line1[1]
    elif (line1[0] == 'plot_var'):
      plot_var=line1[1].split(',')

    # Optional keywords
    elif (line1[0] == 'gmt_offset'):
      gmt_offset = float(line1[1])
      print 'Now setting the gmt offset to {0}'.format(gmt_offset)
    elif (line1[0] == 'plot_var2'):
      plot_var2=line1[1].split(',')
    elif ((line1[0] == 'verbose') or (line1[0] == 'debug')):
      verbose=int(line1[1])
    elif (line1[0] == 'view_request_time'):
      view_request_time = 1

    # Keywords that don't have '=' in it
    else:
      if ((line1[0] == '-h') or (line1[0] == '-sh') or (line1[0] == '--help') or 
          (line1[0] == '--short-help')):
        short_help_message()
        sys.exit()
      elif ((line1[0] == '-v') or (line1[0] == '--verbose')):
        verbose = 1
      elif ((line1[0] == '-vrt') or (line1[0] == '--view_request_time')):
        view_request_time = 1

else:
  print "ERROR: No keywords present in module call."
  short_help_message()
  exit()

# Check to make sure the required keywords are all set (archive times, input file
# and variables to be plotted).
if ((archive_time1 == '') or (archive_time2 == '')):
  print "ERROR: No start and/or end times given."
  short_help_message()
  exit()
if (inputfile == ''):
  print "ERROR: No input file given."
  short_help_message()
  exit
if (len(plot_var) == 0):
  print "ERROR: No variables selected for plotting."
  short_help_message()
  exit()
  
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Convert the given local time to seconds from start of epoch UTC
epoch_time1 = convert_localtime2epochtime(archive_time1)
epoch_time2 = convert_localtime2epochtime(archive_time2)
if (verbose == 1):
  print "epoch_time1: ",epoch_time1
  print "epoch_time2: ",epoch_time2

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Read in data from the input file
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
drst = time.time()  # data read-in start time
# Dig the archived weather station data out of the database file and save it in a 
# list of tuples called datav1.
con = lite.connect(inputfile)
with con:
  cur = con.cursor()
  cur.execute("SELECT * FROM archive;")
  datav1 = cur.fetchall()

# Sort through the list of tuples datav1 and save the data into a dictonary.
# Create an empty dictionary that will eventually store the weather station data
WxStationData = {}
# Create a list of variable names.  NOTE: These are the names I gave the data. 
# "Unknown" data variable names are variables that have data other than 'None', but
# I cannot determine what they are at this time.  "Empty" data variable names are
# variables that only have 'None' in them.
variablelist = ["Epochtime", "USUnits", "SampleInterval", "Barometer", "Pressure", \
                "Altimeter", "InTemp", "OutTemp", "InHumidity", "OutHumidity", \
                "WindSpeed", "WindDir", "WindGust", "WindGustDir", "RainRate", \
                "Rainfall", "Dewpoint", "WindChill", "HeatIndex", "Unknown1", \
                "Empty1", "Empty2", "Empty3", "Empty4", "Empty5", "Empty6", "Empty7", \
                "Empty8", "Empty9", "Empty10", "Empty11", "Empty12", "Empty13", \
                "Empty14", "Empty15", "Empty16", "Empty17", "Empty18", "Empty19", \
                "SignalQuality", "Unknown2", "Unknown3", "Empty20", "Empty21", \
                "Empty22", "Empty23", "Empty24", "Empty25", "Empty26", "Empty27", \
                "Empty28", "Empty29"]

unitslist = ["seconds", "None", "Minutes", "in. Hg.", "in. Hg.", "in. Hg.", \
             "$\degree$F", "$\degree$F", "%", "%", "mph", "degrees", "mph", "dgrees", \
             "in./hr.", "inches", "$\degree$F", "$\degree$F", "$\degree$F", "Unknown", \
             "None", "None", "None", "None", "None", "None", "None", "None", "None", \
             "None", "None", "None", "None", "None", "None", "None", "None", "None", \
             "None", "%", "Unknown", "Unknown", "None", "None", "None", "None", \
             "None", "None", "None", "None", "None", "None"]

# Check to make sure the list has data in it (length of the list is greater than zero).
if (len(datav1) > 0):
  # Loop through the variables to be saved
  for v in range(len(variablelist)):
    # Loop through the rows in the data list
    dummylist = []
    for r in range(len(datav1)):
      dummylist.append(datav1[r][v])
    # Save the data in the dummy list to a dictonary key
    WxStationData[variablelist[v]]=np.array(dummylist)
else:
  # Return an error message and exit the program if there is no input data.
  print "ERROR: No data in input file.  Exiting program."
  exit()

# Add the variable list and units to the dictionary
WxStationData["variablelist"] = variablelist
WxStationData["unitslist"] = unitslist
dret = time.time()  # data read-in end time

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Derive new variables and comput maximum and minimum values for each day.
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
dvst = time.time()  # derived-variable computation start time

# Use the matplotlib.dates.epoch2num() module to create a time array in deciimal days
# since 0001-01-01 00:00 UTC plus 1.0. See https://matplotlib.org/api/dates_api.html 
# for details.
ADdays = mdates.epoch2num(WxStationData["Epochtime"])

# Initialize lists and variables for the computation of once daily values 
# (e.g. max temp).
rain4day = 0.0
rain4day_arr = []
dailydate = []
currday = math.floor(ADdays[0])
maxvars = np.zeros((len(variablelist),int(math.ceil(ADdays[-1]-ADdays[0]))+1))
minvars = np.zeros((len(variablelist),int(math.ceil(ADdays[-1]-ADdays[0]))+1))

# Initialize the maximum and minimum lists
for v in range(len(variablelist)):
  maxvars[v,0] = WxStationData[variablelist[v]][0]
  minvars[v,0] = WxStationData[variablelist[v]][0]

d = 0  # day counter
# Loop through the data
for r in range(len(ADdays)):
  # If the data date is less than the current date plus one (for the next date)
  # plus local timezone offset (gmt_offset).
  if (ADdays[r] < (currday+1.0+gmt_offset)):
    rain4day = rain4day + WxStationData["Rainfall"][r]
    # Loop through the variables
    for v in range(len(variablelist)):
      # Check to see if the current variable value is greater than the current 
      # maximum value.
      if (WxStationData[variablelist[v]][r] > maxvars[v,d]):
        maxvars[v,d] = WxStationData[variablelist[v]][r]
      # Check to see if the current variable value is less than the current 
      # minimum value.
      if (WxStationData[variablelist[v]][r] < minvars[v,d]):
        minvars[v,d] = WxStationData[variablelist[v]][r]
  else:
    # Switched over to a new date.  First save the data from the previous date.
    rain4day_arr.append(rain4day)
    dailydate.append(currday)
    # Reset the currday and rain4day variables for the new date.
    currday = math.floor(ADdays[r])
    rain4day = WxStationData["Rainfall"][r]
    d = d + 1  # increment the day counter
    # Loop through the variables
    for v in range(len(variablelist)):
      maxvars[v,d] = WxStationData[variablelist[v]][r]
      minvars[v,d] = WxStationData[variablelist[v]][r]

# Put whatever data is in the last day in the lists.
rain4day_arr.append(rain4day)
dailydate.append(currday)
dvet = time.time()  # derived-variable computation end time

# Create and fill a new dictionary for the once-daily weather station data
wxddst = time.time()  # create and fill new dictionary start time
WxStationDailyData = {}
varlist2 = []
unitslist2 = []
for v in range(len(variablelist)):
  WxStationDailyData["Max"+variablelist[v]] = maxvars[v,:]
  WxStationDailyData["Min"+variablelist[v]] = minvars[v,:]
  varlist2.extend(["Max"+variablelist[v], "Min"+variablelist[v]])
  unitslist2.extend([unitslist[v], unitslist[v]])
WxStationDailyData["ADDailyDate"] = np.array(dailydate)
WxStationDailyData["Rain4Day"] = np.array(rain4day_arr)
varlist2.extend(["ADDailyDate","Rain4Day"])
unitslist2.extend(["None","inches"])
wxddet = time.time()  # create and fill new dictionary end time
WxStationDailyData["variablelist"] = varlist2
WxStationDailyData["unitslist"] = unitslist2

# Append the new data to the WxStationData dictonary
WxStationData["ADdays"] = ADdays
WxStationData["CumulativeRain"] = WxStationData["Rainfall"].cumsum()
# Add the variable list and units to the dictionary
WxStationData["variablelist"].extend(["ADdays", "CumulativeRain"])
WxStationData["unitslist"].extend(["None", "inches"])

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Depending on whether the user wants to view only the valid data or the whole 
# request frame (the same when the dataset spans the requested time period),
# determine which start and stop times to use for the plotting portion.
if (view_request_time == 1):
  # Determine the local time based on the input dates/times.
  vd1 = time.localtime(epoch_time2)
  vd2 = time.localtime(epoch_time1)
  dtime = epoch_time2 - epoch_time1
  dtime_hours = dtime/3600.0
  if (verbose == 1):
    print "Requested date/time #1: {0}  requested date/tiome #2: {1}".format(time.strftime("%Y-%m-%d %H:%M:%S",vd1), time.strftime("%Y-%m-%d %H:%M:%S",vd2))

  for var in plot_var:
    if (var in WxStationData.keys()):
      # Find the indices that fall within the given start and stop times
      aidx = np.where((WxStationData["Epochtime"] >= epoch_time1) & (WxStationData["Epochtime"] <= epoch_time2))
    elif (var in WxStationDailyData.keys()):
      # Find the indices that fall within the given start and stop times
      bidx = np.where((WxStationDailyData["MinEpochtime"] >= epoch_time1) & (WxStationDailyData["MinEpochtime"] <= epoch_time2))

else:
  for var in plot_var:
    if (var in WxStationData.keys()):
      # Find the indices that fall within the given start and stop times
      aidx = np.where((WxStationData["Epochtime"] >= epoch_time1) & (WxStationData["Epochtime"] <= epoch_time2))

      # Check to make sure there is data found within the specified time frame.
      if (len(aidx[0]) != 0):
        # Determine the difference in the first and last valid time in the dataset
        vd1 = time.localtime(WxStationData["Epochtime"][aidx[0][-1]])
        vd2 = time.localtime(WxStationData["Epochtime"][aidx[0][0]])
        dtime = WxStationData["Epochtime"][aidx[0][-1]] - WxStationData["Epochtime"][aidx[0][0]]
        dtime_hours = dtime/3600.0
        if (verbose == 1):
          print "aidx:: valid date/time #1: {0}  valid date/tiome #2: {1}".format(time.strftime("%Y-%m-%d %H:%M:%S",vd1), time.strftime("%Y-%m-%d %H:%M:%S",vd2))
      else:
        # Return error message and quit the script
        ts1 = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(WxStationDailyData["MinEpochtime"][0]))
        ts2 = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(WxStationDailyData["MaxEpochtime"][-2]))
        print "ERROR: No data available during the specified time period."
        print "         Available time period is {0} to {1}".format(ts1,ts2)
        exit()

    elif (var in WxStationDailyData.keys()):
      # Find the indices that fall within the given start and stop times
      bidx = np.where((WxStationDailyData["MinEpochtime"] >= epoch_time1) & (WxStationDailyData["MinEpochtime"] <= epoch_time2))

      # Check to make sure there is data found within the specified time frame.
      if (len(bidx[0]) != 0):
        # Determine the difference in the first and last valid time in the dataset
        vd1 = time.localtime(WxStationDailyData["MinEpochtime"][bidx[0][-1]])
        vd2 = time.localtime(WxStationDailyData["MinEpochtime"][bidx[0][0]])
        dtime = WxStationDailyData["MinEpochtime"][bidx[0][-1]] - WxStationDailyData["MinEpochtime"][bidx[0][0]]
        dtime_hours = dtime/3600.0
        if (verbose == 1):
          print "bidx:: valid date/time #1: {0}  valid date/tiome #2: {1}".format(time.strftime("%Y-%m-%d %H:%M:%S",vd1), time.strftime("%Y-%m-%d %H:%M:%S",vd2))
      else:
        # Return error message and quit the script
        ts1 = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(WxStationDailyData["MinEpochtime"][0]))
        ts2 = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(WxStationDailyData["MaxEpochtime"][-2]))
        print "ERROR: No data available during the specified time period."
        print "         Available time period is {0} to {1}".format(ts1,ts2)
        exit()

# Print out the time difference in hours between the start and stop time if the 
# verbose mode is on.
if (verbose == 1):
  print 'dtime_hours= ',dtime_hours

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Make the plot
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Set up figure 
f1 = plt.figure(num=1, figsize=(6.4, 3.6), dpi=200, facecolor='w', edgecolor='k')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Plot the data
for var in plot_var:
  # Check to make sure the variable is included in the dictionary and correctly spelled
  if (var in WxStationData.keys()):
    # Check to make sure there is data found within the specified time period.
    if (len(aidx[0]) != 0):
      plt.plot(mdates.epoch2num(WxStationData["Epochtime"][aidx]), WxStationData[var][aidx], label=var)
    else:
      print "WARNING: Variable '{0}' not plotted.".format(var)
      print "         No data available during the specified time period."
  elif (var in WxStationDailyData.keys()):
    # Check to make sure there is data found within the specified time period.
    if (len(bidx[0]) != 0):
      if (var == "Rain4Day"):
        plt.bar(WxStationDailyData["ADDailyDate"][bidx]-0.33, WxStationDailyData[var][bidx], label=var)
      else:
        plt.plot(WxStationDailyData["ADDailyDate"][bidx], WxStationDailyData[var][bidx], label=var)
    else:
      print "WARNING: Variable '{0}' not plotted.".format(var)
      print "         No data available during the specified time period."
  else:
    print "WARNING: Variable '{0}' not plotted.".format(var)
    print "         Variable not found in either WxStationData or WxStationDailyData"
    print "         dictionaries.  Please check whether variable exists or not."

# Grab the current axes handle
ax = plt.gca()

# Add a legend to the plot.
plt.legend(bbox_to_anchor=(1.0,1.1), ncol=4, fontsize=10, frameon=False, handletextpad=0.1)

# Label the x-axis.
ax.set_xlabel("Time (Starting time= {0})".format(time.strftime("%Y-%m-%d %H:%M:%S",vd2)))

# Label the y-axis with the first variale name and its unit.
if plot_var[0] in WxStationData["variablelist"]:
  ax.set_ylabel(plot_var[0] + " [" + WxStationData["unitslist"][WxStationData["variablelist"].index(plot_var[0])] + "]")
elif plot_var[0] in WxStationDailyData["variablelist"]:
  ax.set_.ylabel(plot_var[0] + " [" + WxStationDailyData["unitslist"][WxStationDailyData["variablelist"].index(plot_var[0])] + "]")

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if (plot_var2 != []):
  # Add in second-axis variables, if desired.
  mpl.rcParams['axes.prop_cycle'] = cycler('color', ['black', 'gray', 'firebrick', 'chartreuse', \
                                    'royalblue', 'mediumvioletred'])
  # Clone the x-axis
  ax2 = ax.twinx()
  # Loop through all the variables in plot_var2 list.
  for var in plot_var2:
    # Check to make sure the variable is included in the dictionary and correctly spelled
    if (var in WxStationData.keys()):
      # Check to make sure there is data found within the specified time period.
      if (len(aidx[0]) != 0):
        ax2.plot(mdates.epoch2num(WxStationData["Epochtime"][aidx]), 
                 WxStationData[var][aidx], label=var, linestyle='--')
      else:
        print "WARNING: Variable '{0}' not plotted.".format(var)
        print "         No data available during the specified time period."
    elif (var in WxStationDailyData.keys()):
      # Check to make sure there is data found within the specified time period.
      if (len(bidx[0]) != 0):
        if (var == "Rain4Day"):
          ax2.bar(WxStationDailyData["ADDailyDate"][bidx]-0.33, 
                  WxStationDailyData[var][bidx], label=var)
        else:
          ax2.plot(WxStationDailyData["ADDailyDate"][bidx], 
                   WxStationDailyData[var][bidx], label=var, linestyle='--')
      else:
        print "WARNING: Variable '{0}' not plotted.".format(var)
        print "         No data available during the specified time period."
    else:
      print "WARNING: Variable '{0}' not plotted.".format(var)
      print "         Variable not found in either WxStationData or WxStationDailyData"
      print "         dictionaries.  Please check whether variable exists or not."

  # Label the y-axis with the first variale name and its unit.
  if plot_var2[0] in WxStationData["variablelist"]:
    aunit = WxStationData["unitslist"][WxStationData["variablelist"].index(plot_var2[0])]
    ax2.set_ylabel(plot_var2[0] + " [" + aunit + "]")
  elif plot_var[0] in WxStationDailyData["variablelist"]:
    aunit = WxStationDailyData["unitslist"][WxStationDailyData["variablelist"].index(plot_var2[0])]
    ax2.set_.ylabel(plot_var2[0] + " [" + aunit + "]")

  # Add a legend to the plot.
  plt.legend(bbox_to_anchor=(1.0,1.20), ncol=4, fontsize=10, frameon=False, handletextpad=0.1)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# If the user requests to see the whole time period regardless of data availability, 
# then set the x-axis limits.  Otherwise matplotlib will automatically calcualte the limits
if (view_request_time == 1):
  ax.set_xlim(mdates.epoch2num(epoch_time1),mdates.epoch2num(epoch_time2))

# Depending on the time period requested, format the x-axis tick locations
# If have less than 48 hours (2 days') worth of data to plot.
if (dtime_hours <= 48.0):
  # Format the view of the x-axis major and minor ticks.
  ax.xaxis.set_major_locator(mdates.DayLocator())
  ax.xaxis.set_minor_locator(mdates.HourLocator(np.arange(0, 25, 1)))
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
# If have between 48 and 744 hours to plot (2 days to a week).
elif ((dtime_hours > 48.0) and (dtime_hours <= 168.0)):
  # Format the view of the x-axis major and minor ticks.
  ax.xaxis.set_major_locator(mdates.DayLocator())
  ax.xaxis.set_minor_locator(mdates.HourLocator(np.arange(0, 25, 6)))
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
# If have between 1 to 2 weeks.
elif ((dtime_hours > 168.0) and (dtime_hours <= 336.0)):
  # Format the view of the x-axis major and minor ticks.
  ax.xaxis.set_major_locator(mdates.DayLocator(np.arange(0,32,2)))
  ax.xaxis.set_minor_locator(mdates.HourLocator(np.arange(0, 25, 12)))
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
# If have between 2 weeks and a month.
elif ((dtime_hours > 336.0) and (dtime_hours <= 744.0)):
  # Format the view of the x-axis major and minor ticks.
  ax.xaxis.set_major_locator(mdates.DayLocator(np.arange(0,32,7)))
  ax.xaxis.set_minor_locator(mdates.DayLocator())
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
# If have over a month.
else:
  # Format the view of the x-axis major and minor ticks.
  ax.xaxis.set_major_locator(mdates.MonthLocator(np.arange(0,13,2)))
  ax.xaxis.set_minor_locator(mdates.MonthLocator())
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

# Set the axis tick lengths and widths.
ax.tick_params('both', which='major', length=10, width=1)
ax.tick_params('both', which='minor', length=5, width=1)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Configure the margins so everything is visible. If have a second y-axis, give a 
# little extra space around the figure so that the legends are visible
if (len(plot_var2) > 0):
  plt.tight_layout(pad=2.0)
else:
  plt.tight_layout()

# Get script end time (not counting plot viewing time)
sendtime = time.time()

# Show the graph in a pop-up window.
plt.show()

# Print out script diagnostics, if desired
if (verbose == 1):
  print ' '
  print 'Time required to read in data from input database: {0:.4} seconds'.format(dret-drst)
  print 'Time required to compute derived once-daily variables: {0:.4} seconds'.format(dvet-dvst)
  print 'Time required to create and fill dictionary for derived once-daily variables: {0:.4} seconds'.format(wxddet-wxddst)
  print 'Time required to execute entire script: {0:.4} seconds'.format(sendtime-sstarttime)

  
