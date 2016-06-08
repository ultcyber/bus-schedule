# Local imports
from flask import render_template
from app import app
# Modules
from bs4 import BeautifulSoup
import requests
import re

# Creating the controller for the ZTM site model 

# Parse the ZTM site, find next departure from a given stopID and return an object
def nextBus(busNum, stopID, o, k="B"):
  r = requests.get("http://www.ztm.waw.pl/rozklad_nowy.php?c=182&l=1&a={}&n={}&o={}&k={}".format(busNum, stopID, o, k))
  html_doc = r.text
  soup = BeautifulSoup(html_doc, 'html.parser')
  ztm_html = soup.find(id="RozkladContent")

  nbusreg = re.compile(r'(odjazd za\s)(.*\d+\smin)')
  next_bus = nbusreg.search(str(ztm_html))

  return { "bus" : busNum, "next" : next_bus.group(2) }

def capture_next():
	# Create next departure arrays
	pileckiego = {"title" : "Pileckiego", "departures" : []} 
	stryjenskich = {"title" : "Stryjeńskich", "departures" : []}
	os_wyzyny = {"title" : "Osiedle Wyżyny", "departures" : []}

	pil_bus = ["179", "185"]
	stry_bus = ["192", "504", "503"]

	# Append the departures key for all stops
	for bus in pil_bus:
		pileckiego["departures"].append(nextBus(bus, "3333", "04"))

	for bus in stry_bus:
		stryjenskich["departures"].append(nextBus(bus, "3140", "02"))

	# os_wyzyny requires to change the k parameter, so cannot use the for loop
	os_wyzyny["departures"].append(nextBus("504", "3195", "04", "A"))
	os_wyzyny["departures"].append(nextBus("179", "3195", "04"))

	return [pileckiego, stryjenskich, os_wyzyny]

# Capture the full schedule by looking at the href - it's right there in the "h=" parameter. Return a dictionary hour:[minutes]
def full_schedule(busNum, stopID, o, k="B"):
	r = requests.get("http://www.ztm.waw.pl/rozklad_nowy.php?c=182&l=1&a={}&n={}&o={}&k={}".format(busNum, stopID, o, k))
	html_doc = r.text
	soup = BeautifulSoup(html_doc, 'html.parser')
	
	hour_dict = {}

	hour_regex = re.compile("(h=)(\d+).(\d+)")

	rozklad = soup.find(id="RozkladContent")
		
	for link in rozklad.find_all("a", class_="mi"):
		a = link.get("href")
		b = hour_regex.search(a)
		hour = b.group(2)
		minute = b.group(3)

		if hour in hour_dict:
			hour_dict[hour].append(minute)
		else:
			hour_dict[hour] = [minute]

	return hour_dict

# Routing controllers
@app.route('/')
@app.route('/index')

def index():

	posts = capture_next()
	return render_template("index.html", posts=posts)

@app.route('/pileckiego')

def pileckiego():
	title = "Pileckiego"
	posts_185 = full_schedule("185", "3333", "04")
	posts_179 = full_schedule("179", "3333", "04")

	return render_template("pileckiego.html", posts_185 = posts_185, posts_179 = posts_179, title = title)

@app.route('/os_wyzyny')

def os_wyzyny():
	title = "Osiedle Wyżyny"
	posts_504 = full_schedule("504", "3195", "04", "A")
	posts_179 = full_schedule("179", "3195", "04")
	return render_template("os_wyzyny.html", posts_504 = posts_504, posts_179 = posts_179, title = title)

@app.route('/stryjenskich')

def stryjenskich():
	title = "Stryjeńskich"
	posts_503 = full_schedule("503", "3140", "02")
	posts_504 = full_schedule("504", "3140", "02")
	posts_192 = full_schedule("192", "3140", "02")
	return render_template("stryjenskich.html", posts_503 = posts_503, posts_504 = posts_504, posts_192 = posts_192, title = title)