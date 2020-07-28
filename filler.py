import argparse
import math
import time
from datetime import datetime
from datetime import date
from datetime import timedelta
import sys

# selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

# Defaut configuration (dates are inclusive)
# For date : DD-MM-YYYY
# For hour : HH:MM (Hour, minute)
start_date_str = '22-06-2020'
end_date_str = '08-07-2020'
morning_start_time_str = "09:30"
evening_end_time_str = "18:24"
lunch_break_time_start = "12:30"
lunch_break_time_end = "14:00"
domaine_name = 'DEVELOPPEMENT PLATEFORME'
poste_name = 'MULTIPLATEFORME SOFTW'
enterinator = False
operating_system = 'win64'
adp_url = 'https://adfs.navya.tech/adfs/ls/idpinitiatedsignon.aspx?logintoRP=ADP-HRServices'

# Parser
parser = argparse.ArgumentParser()
parser.add_argument('--start','-s', default=start_date_str,
                   help='Start date in format DD-MM-YYYY')
parser.add_argument('--end', '-e', default=end_date_str,
                   help='End date in format DD-MM-YYYY')
parser.add_argument('--arrival_time', default=morning_start_time_str,
                   help='Morning arrival time start in HH:MM 24-hours format')
parser.add_argument('--leave_time', default=evening_end_time_str,
                   help='Evening leave time start in HH:MM 24-hours format')
parser.add_argument('--lunch_start', default=lunch_break_time_start,
                   help='Lunch break time start in HH:MM 24-hours format')
parser.add_argument('--lunch_end', default=lunch_break_time_end,
                   help='Lunch break time end in HH:MM 24-hours format')
parser.add_argument('--domaine', default=domaine_name,
                   help='Domaine name for activity information. Available in the scroll down menu in ADP. Between " "')
parser.add_argument('--poste', default=poste_name,
                   help='Poste name for activity information. Available in the scroll down menu in ADP. Between " "')
parser.add_argument('--enterinate','-Z', action='store_true', default=enterinator,
                   help='Enterinate after filling')
parser.add_argument('--os','-o', action='store', default=operating_system,
                   help='Operating system. Values : win64 win32 linux64 mac64')
parser.add_argument('--url','-u', action='store', default=adp_url,
                   help='ADP url.')

args = vars(parser.parse_args())

# Re-map variables
start_date_str = args['start']
end_date_str = args['end']
morning_start_time_str = args['arrival_time']
evening_end_time_str = args['leave_time']
lunch_break_time_start = args['lunch_start']
lunch_break_time_end = args['lunch_end']
domaine_name = args['domaine']
poste_name = args['poste']
enterinator = args['enterinate']
adp_url = args['url']

drivers_paths = {'win64': 'win64/chromedriver.exe',
                'win32': 'win32/chromedriver.exe',
                'linux64': 'linux64/chromedriver',
                'mac64': 'mac64/chromedriver'}

driver_path = drivers_paths[args['os']]

# Output brief on variables
if enterinator:
    enterin_status = 'ON'
else:
    enterin_status = 'OFF'

print("\n\nStarting ADPROUT automatic filling with ENTERINATION \x1b[6;30;42m", enterin_status,'\x1b[0m\n'
      'On time interval : [',start_date_str,'-',end_date_str,']','\n'
      'You worked each day from\x1b[6;30;42m',morning_start_time_str,'to',evening_end_time_str,'\x1b[0m\n'
      'And ate like the little piggy you are from\x1b[6;30;42m',lunch_break_time_start,'to',lunch_break_time_end,'\x1b[0m\n')
sys.stdout.flush()

# Browser driver instance creation. Here only works with chrome for Windows.
# Chrome drivers for linux and mac available in the repo, change the binary name here
browser = webdriver.Chrome(driver_path)
#Go to ADP website. If site not found, change URL to one that works for you
browser.get(adp_url)
original_window = browser.current_window_handle #save tab id

# Open drown down menu "Temps et Activites" and click the link "Gestion des temps..."
wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "menu_2_navItem_label")))
link1 = browser.find_element_by_id("menu_2_navItem_label")
link1.click()
wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "dijit_layout_ContentPane_1")))
link2 = browser.find_element_by_id("dijit_layout_ContentPane_1")
link2.click()

# Wait for new tab to open and switch tab
wait(browser, 15).until(EC.number_of_windows_to_be(2))
for window_handle in browser.window_handles:
        if window_handle != original_window:
            browser.switch_to.window(window_handle)
            window_2 = window_handle
            break

# Open drown down menu "Temps / Activites" and click the link "Déclarer présence/act"
wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "revit_navigation_NavHoverItem_1_label")))
link3 = browser.find_element_by_id("revit_navigation_NavHoverItem_1_label")
link3.click()
wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "revit_navigation_NavItem_2_label")))
link4 = browser.find_element_by_id("revit_navigation_NavItem_2_label")
link4.click()

## Date manipulation
# Put entry dates in date instance
start_date = datetime.strptime(start_date_str, "%d-%m-%Y").date()
end_date = datetime.strptime(end_date_str, "%d-%m-%Y").date()
wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "btnPrev")))
wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "btnNext")))

# If adp dates display is ahead of start filling date, let's go back in time Morty
while True:
    # Read start date of ADP page
    start_date_adp_page = browser.find_element_by_id("dat_deb_fin").text
    assert (start_date_adp_page.split()[1].find('/'))
    start_adp_date = datetime.strptime(start_date_adp_page.split()[1].replace('/', '-'), "%d-%m-%Y").date()

    # Click button
    if ((start_date - start_adp_date).days < 0):
        browser.find_element_by_id("btnPrev").click()
    elif ((start_date - start_adp_date).days > 6):
        browser.find_element_by_id("btnNext").click()
    else:
        wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "btnNext")))
        wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "btnPrev")))
        break

    wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "btnNext")))
    wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "btnPrev")))

# Loop over weeks until end date is reached
while True:
    # Read start/end date of ADP page
    date_adp_page = browser.find_element_by_id("dat_deb_fin").text
    assert (date_adp_page.split()[1].find('/'))
    start_adp_date = datetime.strptime(date_adp_page.split()[1].replace('/', '-'), "%d-%m-%Y").date()
    assert (date_adp_page.split()[3].find('/'))
    end_adp_date = datetime.strptime(date_adp_page.split()[3].replace('/', '-'), "%d-%m-%Y").date()

    ## Get reference to all days start and end timestep fields
    # Array of each half-day's offset to Monday morning
    days_array = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    week_array = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    week_names = ["Monday morning", "Monday Evening", "Tuesday morning", "Tuesday Evening", "Wednesday morning",
                  "Wednesday Evening", "Thursday morning", "Thursday Evening", "Friday morning", "Friday Evening"]
    # Get html table of the page
    time.sleep(1)
    table = browser.find_element_by_id("conteneur")
    rows = table.find_elements_by_tag_name("tr")
    row = rows[45]
    cells = row.find_elements_by_tag_name("td")
    assert (len(cells) == 15)
    # Loop over each cell to check if it is a RTT/Vacations Day/Paid leave, disease,...
    for i in range(10):
        if cells[i].text in {"AC", "JS", "JM", "JF", "CP", "AA", "MA"}:
            week_array.remove(i)
            print(week_names[i], "will be ignored [Day not worked]")

    # Truncate week array if the start of the desired period is within the week
    if (start_adp_date < start_date):
        week_array = list(filter(lambda x: (x >= 2 * (start_date - start_adp_date).days), week_array))
        print("Half-days before", week_names[2 * (start_date - start_adp_date).days],
              "will be ignored [Out of filling interval]")
        # Truncate week array if the end of the desired period is within the week
    if (end_adp_date > end_date):
        week_array = list(filter(lambda x: (x <= 13 - 2 * (end_adp_date - end_date).days), week_array))
        print("Half-days after", week_names[13 - 2 * (end_adp_date - end_date).days],
              "will be ignored [Out of filling interval]")

    # Get link to timestep field of each half day which was not filtered out
    # Mornings timesteps filling
    mornings = list(filter(lambda x: (x % 2 == 0), week_array))
    for i in range(len(mornings)):
        # Mornings arrival timesteps filling
        date = start_adp_date + timedelta(days=mornings[i] / 2)
        id_morning = date.strftime('%d') + '/' + date.strftime('%m') + '/' + date.strftime('%Y') + '_0'
        wait(browser, 0.1).until(EC.element_to_be_clickable((By.ID, id_morning)))
        browser.find_element_by_id(id_morning).send_keys(morning_start_time_str)
    # Lunch break start timesteps filling
        id_lunch_start = date.strftime('%d') + '/' + date.strftime('%m') + '/' + date.strftime('%Y') + '_1'
        wait(browser, 0.1).until(EC.element_to_be_clickable((By.ID, id_lunch_start)))
        browser.find_element_by_id(id_lunch_start).send_keys(lunch_break_time_start)

    # Afternoons timesteps filling
    afternoons = list(filter(lambda x: (x % 2 == 1), week_array))
    for i in range(len(afternoons)):
        date = start_adp_date + timedelta(days=math.floor(afternoons[i] / 2))
        # Lunch break start timesteps filling
        id_lunch_end = date.strftime('%d') + '/' + date.strftime('%m') + '/' + date.strftime('%Y') + '_2'
        wait(browser, 0.1).until(EC.element_to_be_clickable((By.ID, id_lunch_end)))
        browser.find_element_by_id(id_lunch_end).send_keys(lunch_break_time_end)
        # Leave time filling
        id_leave = date.strftime('%d') + '/' + date.strftime('%m') + '/' + date.strftime('%Y') + '_3'
        wait(browser, 0.1).until(EC.element_to_be_clickable((By.ID, id_leave)))
        browser.find_element_by_id(id_leave).send_keys(evening_end_time_str)
    # Save
    wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "savBtn_label")))
    save_button = browser.find_element_by_id("savBtn_label")
    save_button.click()

    # Fill activity
    time.sleep(2)
    table = browser.find_element_by_id("conteneur")
    rows = table.find_elements_by_class_name("detailJournalier.detail_pre_saisi")
    rows[0].click()

    wait(browser, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.dijitTabInnerDiv")))
    activite_tab = browser.find_elements_by_class_name("tabLabel")[4]
    activite_tab.click()
    time.sleep(0.3)

    # Fill activity for each day
    for i in range(5):
        # Check if "+" activity button available
        activity_button = False
        try:
            wait(browser, 1).until(EC.element_to_be_clickable((By.CLASS_NAME, "popup_ajout_pre")))
            activity_button = True
        except:
            print('No work time to fill on', days_array[i])
            pass
        # check if time already filled
        already_filled = False
        try:
            wait(browser, 0.1).until(EC.element_to_be_clickable((By.CLASS_NAME, "c.Update_act")))
            already_filled = True
        except:
            pass
        if activity_button and not already_filled:
            add_activity = browser.find_element_by_class_name("popup_ajout_pre")
            add_activity.click()

            # Select "Domaine" option
            wait(browser, 15).until(EC.presence_of_element_located((By.ID, 'SEL_LIEUX_ANA')))
            domaine = Select(browser.find_element_by_id('SEL_LIEUX_ANA'))
            # Can be selected by visible text or by id. Inspect the html page for the ids/names
            domaine.select_by_visible_text(domaine_name)
            # Select "Poste" option
            wait(browser, 15).until(EC.presence_of_element_located((By.ID, 'SEL_POSTE_ANA')))
            poste = Select(browser.find_element_by_id('SEL_POSTE_ANA'))
            # Can be selected by visible text or by id. Inspect the html page for the ids/names
            time.sleep(0.4)
            #TODO: find a way to wait for scrollable menu option to be selectable instead of active wait
            poste.select_by_visible_text(poste_name)

            # Fill duration with global duration of the day
            global_duration_sentence = browser.find_element_by_id('decl_popup').text.split()
            global_duration = global_duration_sentence[len(global_duration_sentence) - 1]

            duration_field = browser.find_element_by_id('VALEUR')
            duration_field.send_keys(Keys.CONTROL + 'a')
            duration_field.send_keys(global_duration)
            # Validation button
            wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "ValiderPopupAct_label")))
            browser.find_element_by_id("ValiderPopupAct_label").click()

            wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "EnregistrerAct_label")))
            save_button = browser.find_element_by_id("EnregistrerAct_label")
            save_button.click()

        # Go to next day of the week
        wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "popup_dj_next_date")))
        next_day_button = browser.find_element_by_id("popup_dj_next_date").click()

    wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "dj_close_label")))
    back_button = browser.find_element_by_id("dj_close_label").click()

    # If the end of the asked period is not reached, go to the next page
    if ((end_date - end_adp_date).days <= 0):
        # Enterinate if required
        if enterinator:
            wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "entBtn_label")))
            enterinate_button = browser.find_element_by_id("entBtn_label").click()
            # Enter end date before enterination on last week
            wait(browser, 15).until(EC.element_to_be_clickable((By.ID, 'date_enteriner')))
            date_formatted = end_date.strftime('%d') + '/' + end_date.strftime('%m') + '/' + end_date.strftime('%Y')
            enterination_date = browser.find_element_by_id('date_enteriner')
            enterination_date.send_keys(Keys.CONTROL + 'a')
            enterination_date.send_keys(date_formatted)
            wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "entBtn2_label")))
            enterinate_button2 = browser.find_element_by_id("entBtn2_label").click()

        break
    else:
        # Enterinate if required
        if enterinator:
            wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "entBtn_label")))
            enterinate_button = browser.find_element_by_id("entBtn_label").click()
            wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "entBtn2_label")))
            enterinate_button2 = browser.find_element_by_id("entBtn2_label").click()

        wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "btnNext")))
        browser.find_element_by_id("btnNext").click()
        wait(browser, 15).until(EC.element_to_be_clickable((By.ID, "btnNext")))

print("That's all Folks !!!")



