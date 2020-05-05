# Requirements
Selenium : http://www.selenium.dev
'pip install selenium'
Google Chrome browser.

# ADP Automatic filler
Works by default with chrome browser on windows. You can switch the browser driver according to your OS 
by unzipping the right driver in the repo and changing its reference in the code. 

## Not using Chrome ?

If you want to use a different browser, check selenium page to get the download links to the right driver
and put it in the repo. Change the reference in the script to use the right driver. A little extra compatibility work might be needed.

# Arguments

'-e', '--enterinate'    Activate enterination

# INSTRUCTIONS /!\ Important

first open filler.py with a text editor and fill the configuration variables according to your needs.
Then run 'py filler.py' in a bash

This tool is basically a clickbot on a webbrowser. Avoid having your mouse over the browser when the bot is running
as unvolontarily hovering over a menu could prevent other actions. Timeout errors can happen if your connexion
or computer is too slow. Try running the tool again as those errors are not happening consistently.

Once the browser is launched after running filler.py you can reduce/unfocus the browser window.

# Resetter

run resetter.py to erase all previously inputted data. This does not work if there are "Enterinated" periods over the main period specified in configuration variables.

# CONFIGURATION

Run script with -h to get the detail of the required configuration. As the script can be launched specifying every option,
it is easier to edit the script and change the default values according to you as they will not change much for a same person.

I only recommend to leave the enterinator option default value on False as its consequences cannot be reversed.

start_date_str =            Date on which the filling should start (included) "JJ-MM-YYY"
end_date_str =              Date on which the filling should end (included) "JJ-MM-YYY"
morning_start_time_str =    Arrival time in the morning "HH:MM" in 24 hours format
evening_end_time_str =      Leave time in the evening "HH:MM" in 24 hours format
lunch_break =               Toggle lunch break time precision (If false, the lunch break minimal time of 45 mins will automatically be considered by ADP)
lunch_break_time_start =    Lunch break start time "HH:MM" in 24 hours format
lunch_break_time_end =      Lunch break end time "HH:MM" in 24 hours format
domaine_name =              Name of the option in the "Domaine" menu
poste_name =                Name of the option in the "Projet" menu
enterinator =               To enterinate or not. Better to try without first