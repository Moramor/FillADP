# Requirements
Selenium : http://www.selenium.dev
'pip install selenium'
# ADP Automatic filler
Works by default with chrome browser on windows. You can switch the browser driver according to your OS 
by unzipping the right driver in the repo and changing its reference in the code. 
If you want to use a different browser, check selenium page to get the download links to the right driver
and put it in the repo.


#INSTRUCTIONS /!\ Important

first open filler.py with a text editor and fill the configuration variables according to your needs.
Then run 'py filler.py' in a bash

This tool is basically a clickbot on a webbrowser. Avoid having your mouse over the browser when the bot is running
as unvolontarily hovering over a menu could prevent other actions (for instance). Timeout errors can happen if your connexion
or computer is too slow. Try launching the tool again as they are not-systematic.

Once the browser is launched when running filler.py you can reduce/unfocus the browser window.