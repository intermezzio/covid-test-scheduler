# Covid Test Scheduler

Automatically schedule your Covid tests using Olin's new testing platform!

## Installation

Clone this repository and install the dependencies (requires Python)

```sh
pip3 install -r requirements.txt
```

Then install the geckodriver, something that lets you create a Firefox
window in Python. This can be downloaded from the 
[official page](https://github.com/mozilla/geckodriver/releases) or
[this autoinstaller](https://pypi.org/project/geckodriver-autoinstaller/).

## Usage

There's a `preferences.json` file with three things to specify:

| Field | Description |
|:---:|:---:|
| email | your email address or username for the testing site |
| password | for logging onto the platform - this is only stored locally and used to log in on your computer |
| day | a day of the week you want the test on - not including this sets it to the next possible appointment |

To run the code, run the main Python script:

```sh
python3 schedule.py
```

### Note

To prevent a bad test from being scheduled, this script intentionally stops right before
confirming the appointment. To fully schedule the appointment **you have to click the
last confirm button** at the end.