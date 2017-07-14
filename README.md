# read_weewx

  NAME: 
    - read_weewxdata.py
    - read_weewxdata_p3.py

  PURPOSE:
    To read in data from a weewx.sdb file and plot selected variables.

  VERSIONS:
    - read_weewxdata.py is developed for python2. Known to work with Python 2.7.11
        and Matplotlib 1.5.1
    - read_weewxdata_p3.py is developed for python3. Known to work with Python 3.5.2
        and Matplotlib 2.0.2

  CALLS:
    Built-in Python modules cycler, numpy, math, matplotlib/
      matplotlib.pyplot/matplotlib.dates, time, sqlite3, and sys

  MODIFICATIONS:
    - Andrea Neumann <andrea.neumann2@gmail.com> 10 July 2017: Written
    - Andrea Neumann <andrea.neumann2@gmail.com> 12 July 2017: Debugged, added 
        command-line keyword input, removed hard-coded example code, and added
        a bar graph option for the rain4day variable.  Also started on creating
        module header information and documentation.
    - Andrea Neumann <andrea.neumann2@gmail.com> 13 July 2017: Added much of the
        module header information, started working on adding plotting on a second
        y-axis capability, and added another color cycle for the second y-axis 
        variables.

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
    - Made use of online sample code from http://zetcode.com/db/sqlitepythontutorial/ 
      and https://groups.google.com/forum/#!msg/weewx-user/Plw2MjoV8NY/wz1XH45XDwAJ
    - Weather Data order help came from: http://sospilot.readthedocs.io/en/latest/weatherstation.html
    - https://docs.python.org/2/library/time.html was a very helpful website for the
      time conversion code.
    - Code for setting a default matplotlib color cycle came from:
       https://matplotlib.org/examples/color/color_cycle_demo.html and 
       https://matplotlib.org/users/dflt_style_changes.html#colors-in-default-property-cycle

