# IMPORTANT

Whenever your pull a new version, run

    python -m pip install .

In a bash in the repo's folder. This will ensure the script is updated when you run it.

# Requirements

    - Google Chrome browser.
    - Already have connected to ADP in Chrome with your account and have an automatic connexion set up

# ADP Automatic filler
Works by default with chrome browser on windows. You can switch the browser driver according to your OS 
by unzipping the right driver in the repo and changing its reference in the code. 

# Resetter

run 

    py resetter.py
to reset all non-enterinated data from the specified period.

## Not using Chrome ?

If you want to use a different browser, check selenium page to get the download links to the right driver
and put it in the repo. Change the reference in the script to use the right driver. A little extra compatibility work might be needed.

# Arguments

Run script with -h to get the detail of the arguments. As there are many arguments, it is easier to edit the config.yml file
and change the default values according to you as they will not change much for a same person.

# INSTRUCTIONS

First, open config.yml with a text editor and fill the configuration variables according to your needs.
If this is your first use of FillADP, also fill adprout/last_filled with the date of the last enterinated entry in your ADP calendar.
The command will be named adprout (ADP rapid organizer and uploader of timestamps)

Then open a bash into the repo root folder and enter
 
    python -m pip install .     # This installs the adprout command
then

    adprout         # This starts filling your adp with enterination OFF
    
After running adprout once and checking everything was correctly filled, you can now run

    adprout -Z      # This starts filling your adp with enterination ON

This tool is basically a clickbot on a webbrowser. Avoid having your mouse over the browser when the bot is running
as unvolontarily hovering over a menu could prevent other actions. Timeout errors can happen if your connexion
or computer are too slow. Try running the tool again as those errors are not happening consistently.

Once the browser is launched after running the command you can reduce/unfocus the browser window.

# CONFIGURATION

I only recommend to leave the enterinator option default value on False as its consequences cannot be reversed.

    start_date_str =            Date on which the filling should start (included) "JJ-MM-YYY". Do not start on a Saturday/Sunday
    end_date_str =              Date on which the filling should end (included) "JJ-MM-YYY"
    morning_start_time_str =    Arrival time in the morning "HH:MM" in 24 hours format
    evening_end_time_str =      Leave time in the evening "HH:MM" in 24 hours format
    lunch_break =               Toggle lunch break time precision (If false, the lunch break minimal time of 45 mins will automatically be considered by ADP)
    lunch_break_time_start =    Lunch break start time "HH:MM" in 24 hours format
    lunch_break_time_end =      Lunch break end time "HH:MM" in 24 hours format
    domaine_name =              Name of the option in the "Domaine" menu
    poste_name =                Name of the option in the "Projet" menu
    enterinator =               To enterinate or not. Better to try without first
    operating_system =          Your operating system between those options : 'win64','win32','linux64','mac64'. Using another OS ? Too bad
