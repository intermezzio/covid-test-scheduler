import time
import json
from datetime import datetime
from selenium import webdriver

with open("preferences.json", "r") as infile:
	config = json.load(infile)

EMAIL = config["email"]
PASSWORD = config["password"]
try:
	DAY = config["day"].lower().strip()
	DAY_SET = DAY in {"sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"}
except:
	DAY_SET = False

## Login

# Reach the login page
login_url = "https://crsp-testing.broadinstitute.org/login"

driver = webdriver.Firefox();

driver.get(login_url)
driver.maximize_window()
time.sleep(2)

# Type in username / email
username_button = driver.find_element_by_id("email-or-phone")
username_button.send_keys(EMAIL)

submit_button = driver.find_element_by_id("submit")
submit_button.click()
time.sleep(1) # there's some animation thing here

# Type in password
password_button = driver.find_element_by_id("password")
password_button.send_keys(PASSWORD)

submit_button = driver.find_element_by_id("submit")
submit_button.click()
time.sleep(2)

## Choose Appointment Type
schedule_url = "https://crsp-testing.broadinstitute.org/appointment/new/"
driver.get(schedule_url)
time.sleep(2)

next_button = driver.find_element_by_css_selector("button[type=\"submit\"]")
driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
next_button.click()
time.sleep(3)

## Schedule the test time
if DAY_SET:
	# Click the date picker
	day_button = driver.find_element_by_css_selector("button[aria-label=\"select date\"]")
	driver.execute_script("arguments[0].scrollIntoView(true);", day_button)

	day_button.click()
	time.sleep(0.5)

	# Get current month
	month_header = driver.find_element_by_css_selector("div.MuiPickersCalendarHeader-switchHeader div p")
	month, year = month_header.get_attribute("innerHTML").split()

	# Get available days
	dates = dict()
	available_dates = driver.find_elements_by_css_selector("div.MuiPickersSlideTransition-transitionContainer " +
		"div.MuiPickersCalendar-week div[role=\"presentation\"] button:not(.MuiPickersDay-dayDisabled) p")
	
	# Store dates in a usable format
	for date in available_dates:
		date_int = int(date.get_attribute("innerHTML"))
		dates[date_int] = date
	possible_days = list(dates.keys())
	possible_days.sort()
	print(f"Possible days: {month} {possible_days}, {year}")

	# Check which available day(s) are on the right day of the week, then choose the first one
	for date in possible_days:
		# Humorous weekday detector
		date_str = f"{month} {date}, {year}"
		weekday = datetime.strptime(date_str, r"%B %d, %Y").strftime("%A").lower()
		print(date, weekday)
		if DAY == weekday:
			best_date = date
			print(f"Best day: {month} {best_date}, {year}")
			break
	else:
		print("No good date found this month. Continue on the site and choose a day you'd like.")

	# Click the best date on the date picker
	correct_date = dates[best_date]
	correct_date.click()
	time.sleep(0.5)
else:
	print("No weekday selected, choosing the earliest time slot")

# Click the next button after choosing a time for the test
next_button = driver.find_element_by_css_selector("button[type=\"submit\"]")
driver.execute_script("arguments[0].scrollIntoView(true);", day_button)
next_button.click()
print("The process completed without errors. Click confirm on the site to schedule the appointment.")