import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
import urllib

import jinja2
import os
import time


from models import Event


def create_calendar_url(event):
    date = datetime.datetime.strptime(event.event_date, '%Y-%m-%d').strftime('%Y%m%d')
    time = datetime.datetime.strptime(event.event_time, '%H:%M')
    start_time = time.strftime('%H%M%S')
    end_time = (time + datetime.timedelta(hours = 2)).strftime('%H%M%S')
    date_and_time = date + 'T' + start_time + '/' + date + 'T' + end_time
    domain = "https://calendar.google.com/calendar/r/eventedit"
    event_details = {
        "text" : event.event_name,
        "dates": date_and_time,
        "details": event.event_des,
        "sf": "true",
        "location": event.event_location,
    }
    data = urllib.urlencode(event_details)
    url = "%s?%s" % (domain, data)
    return url


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class IntroPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template("/templates/intropage.html")
        user = users.get_current_user()
        login_url = None
        email_address = None
        if user:
            email_address = user.nickname()
        login_url = users.create_login_url('/main')
        template_vars = {
            "isUser": user,
            "email": email_address,
            "login_url": login_url,
            }
        self.response.write(template.render(template_vars))
    def post(self):
        template = jinja_env.get_template('/templates/index.html')



class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template("/templates/index.html")
        user = users.get_current_user()
        logout_url = None
        logout_url = users.create_logout_url('/')
        template_vars = {
            "logout_url" : logout_url,
        }
        self.response.write(template.render(template_vars))


class AddEventPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template("templates/addevent.html")

        logout_url = None
        logout_url = users.create_logout_url('/')
        template_vars = {
            "logout_url" : logout_url,
        }
        self.response.write(template.render(template_vars))
    def post(self):
        host_name = self.request.get("host_name")
        event_name = self.request.get("event_name")
        event_time = self.request.get("event_time")
        event_location = self.request.get("event_location")
        event_type = self.request.get("event_type")
        # event_image = self.request.get("event_image")
        event_des = self.request.get("event_des")
        host_email = self.request.get("host_email")

        event_post = Event(host_name=host_name, event_name=event_name, event_time=event_time,
        event_location=event_location, event_des=event_des, host_email=host_email, event_type=event_type)
        event_post.put()

        if event_type == "sports":
            self.redirect('/sports')
            time.sleep(.5)
        elif event_type == "clubs":
            self.redirect('/clubs')
            time.sleep(.5)
        elif event_type == "academics":
            self.redirect('/academics')
            time.sleep(.5)
        else:
            self.redirect('/socialevents')
            time.sleep(.5)







class SportsPage(webapp2.RequestHandler):
    def get(self):



        self.response.headers['Content-Type'] = 'text/html'
        sports_events = Event.query(Event.event_type=='sports').fetch()
        template_vars = {
            "sports_events":sports_events,
        }
        template = jinja_env.get_template("templates/sports.html")
        self.response.write(template.render(template_vars))

class AcademicsPage(webapp2.RequestHandler):
    def get(self):


        self.response.headers['Content-Type'] = 'text/html'
        academics_events = Event.query(Event.event_type=='academics').fetch()
        template_vars = {
            "academics_events":academics_events,
        }
        template = jinja_env.get_template("/templates/academics.html")
        self.response.write(template.render(template_vars))

class ClubsPage(webapp2.RequestHandler):
    def get(self):
        event_type = self.request.get('event_type')

        self.response.headers['Content-Type'] = 'text/html'
        clubs_events = Event.query(Event.event_type=='clubs').fetch()
        template_vars = {
            "clubs_events":clubs_events,
        }
        template = jinja_env.get_template("/templates/clubs.html")
        self.response.write(template.render(template_vars))

class SocialEventsPage(webapp2.RequestHandler):
    def get(self):
        event_type = self.request.get('event_type')

        self.response.headers['Content-Type'] = 'text/html'
        social_events = Event.query(Event.event_type=='parties').fetch()
        template_vars = {
            "social_events":social_events,
        }
        template = jinja_env.get_template("/templates/socialevents.html")
        self.response.write(template.render(template_vars))

class YourEventsPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template("/templates/yourevents.html")
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', IntroPage),
    ('/main', MainPage),
    ('/addevent', AddEventPage),
    ('/sports', SportsPage),
    ('/academics', AcademicsPage),
    ('/clubs', ClubsPage),
    ('/socialevents', SocialEventsPage),
    ('/yourevents', YourEventsPage)

], debug=True)
