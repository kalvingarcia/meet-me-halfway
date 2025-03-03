# Meet Me Halfway
This was a project created with a team in my undergraduate experience. The project and assignment
was used to simulate creating designing a project in a team, with stakeholders involved. We had
weekly scrum meetings, stakeholder meetings, conducted research on our target audience, and created
presentations of the project and data for meetings.

**Members:**
- Cameron Smyrl (smyrlcam)
- Matt Curtin (MattCurtin12)
- Kalvin Garcia (OchaKaru)
- Wesley Glover (WesleyGlover)
- Logan Wheeler (BraysonWheeler)

For the course, we were assigned a project to create, rather than coming up an idea ourselves.

## The Concept
Sometimes 2 people need to meet halfway (more or less) between where they are. Common examples are 
custody exchanges or trying to meet a relative/friend who is passing through on a trip. It should 
have features like noting any favorites, suggesting nearby restaurants or police stations. Users 
need to be able to enter their address and the app gives them options on where to meet (that are 
near something – so not in the middle of nowhere) based on their needs (e.g., at a police station).

## My Role
For this project, I was the lead designer and frontend developer. I focused myself on doing research
for the best user experience possible when using out application while creating a frontend that was
completely modular from the backend.

First I began with wireframing each page of our app, so we could have the concepts in place. To support
our cross-platform team, we opted to use Kivy for the UI developement. After doing more research, I found
Google's Material Design paradigm which focused on creating a consistent fontend experience for users.
Luckily, an open source project existed for creating Material Design focused Kivy projects, called KivyMD.

## Dependencies:
  Kivy: <br />
    `pip install kivy` <- also installs kivy-garden, I think. <br />
  KivyMD (no longer optional): <br />
    `pip install kivymd` <br />
  Twisted: <br />
    `pip install twisted` <br />
  MapView: <br />
    `pip install mapview` <br />
    `garden install mapview` (optional) <br />
  KivyCalendar: <br />
    `pip install KivyCalendar` (needs modification to be compatible with Python v3.0+) <br />
  Geopy: <br />
    `pip install geopy` <br />
  Geocoder:<br />
    `pip install geocoder` <br />
  Py3-validate-email:<br />
    `pip install py3-validate-email` <br />
  MySQL:<br />
    `pip install mysql-connector-python` <br />
  Scipy:<br />
    `pip install scipy` <br />

"Updating" KivyCalendar: [Stack Overflow](https://stackoverflow.com/questions/48518358/getting-error-no-module-named-calendar-ui-even-though-kivycalendar-has-been)

1. Go here: KivyCalendar/__init__.py <br />
    change `from calendar_ui import DatePicker, CalendarWidget` <br />
    to `from .calendar_ui import DatePicker, CalendarWidget` <br />

2. Then go here: KivyCalendar/calendar_data.py <br />
    change `from calendar import TimeEncoding, month_name, day_abbr, Calendar, monthrange` <br />
    to `from calendar import month_name, day_abbr, Calendar, monthrange` <br />
    add this: <br />

   ```python
    import locale as _locale

    class TimeEncoding:
      def __init__(self, locale):
        self.locale = locale

      def __enter__(self):
        self.oldlocale = _locale.setlocale(_locale.LC_TIME, self.locale)
        return _locale.getlocale(_locale.LC_TIME)[1]

      def __exit__(self, *args):
        _locale.setlocale(_locale.LC_TIME, self.oldlocale)
   ```

3. Finally go here: KivyCalendar/calendar_ui.py <br />
      change `import calendar_data as cal_data` <br />
      to `from . import calendar_data as cal_data` <br />

   You're done! Go on and prosper, the UI should run.
