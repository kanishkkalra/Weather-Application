# Name - Kanishk Kalra
# Student ID - C0832722

import pyowm
import PySimpleGUI as sg
from datetime import date

# Declaring variables
temperature = ""
tempC = ""
cityW = ""
tempInC = ""

# This method will get the current weather based on the city entererd
def getWeather(city):
    # declaring valriables as global
    global temperature
    global tempInC
    global tempC
    global cityW

    # Fetching data from OWM api using api key
    owm = pyowm.OWM("73b00eb66f1812b4521baf6eb5055d40")
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city) # Fetching data of the city entered
    w = observation.weather

    return w # returing the enture weather object

# Setting window theme to dar
sg.theme('Dark')

# Preparing layout the window that will take user input
layout = [
    [sg.Text('For current weather, \nplease enter City name in \'City, Province\' format.')],
    [sg.Text('City', size=(10,1)),sg.InputText()],
    [sg.Submit(), sg.Cancel()]
]

# Displaying window that takes user data
window = sg.Window('Enter City Name', layout)
event, values = window.read() # Reading events and values entered
cityName = str(values[0])
w = getWeather(cityName) # Calling getWeather function to fetch weather data
window.close() # Closing window
# Calculatin temperature in Fahrenheit w.temperature('fahrenheit') wasnt working for me
tempInF = str(round((w.temperature()['temp'] - 273.15) * 9/5 + 32,2))

# Creating new window. This window will show the weather data
layout = [
    # Displaying termerature in celcius with today's date and city name entered
    [sg.Text(str(round(w.temperature()['temp'] - 273.15,2)) + " °C", font=("Helvetica", 17)), sg.Text(values[0]+"\n"+str(date.today()),size=(20,2), font=("Helvetica", 12), justification="right")],
    # Displaying temperature in fahrenheit
    [sg.Text(tempInF+" °F",font=("Helvetica", 17))],
    # Displaying detailed status in proper case
    [sg.Text(w.detailed_status.title(), font=("Helvetica", 12))],
    # Displaying wind speed
    [sg.Text("Wind: "+str(w.wind()["speed"])+" km/h")],
    # Displaying humidity
    [sg.Text("Humidity: "+str(w.humidity)+" %")],
    # [sg.Text(w.weather_icon_url())], # This returns a url that contains the image in relation to current weather. Like sun for sunny, clouds for cloudy. Wasnt able to display image on window from url
    # Timer starts from 30 minutes. Each second here is slower than a second is actual world
    [sg.Text(size=(30,1),font=("Helvetica", 12) , key="_timer_")],
    [sg.Button("Close")]
]

# Displaying window with the weather data
window = sg.Window('Current Weather', layout)
counter = 0

# Loop to keep the window open
while True:
    # Reading event and values every 10 miliseconds
    event, values = window.read(10)
    # Variable to see the value of minutes
    timerStop = (counter//100)//60
    # Updating time timer key in the layout, Showing minutes and seconds
    # This timer is slower than actual real world timer. 10 seconds on this timer is equal to 12 seconds on real world. 
    # This timer is not suitable for actual production work 
    window['_timer_'].update('Updating current weather in: '+'{:02d}:{:02d}'.format(29 - ((counter // 100) // 60), 59 -  ((counter // 100) % 60)))
    counter+=1
    # End program if user closes window or
    # presses the OK button
    if event == "Close" or event == sg.WIN_CLOSED:
        break
    
    # Update the details if timer reaches 30 minutes
    if timerStop == 30:
        
        counter = 0
        # Closing the previous window
        window.close()
         # Generating same layout with updated values
        layout = [
            # [sg.Text(values[0],size=(30,1), font=("Helvetica", 15))],
            [sg.Text(str(round(w.temperature()['temp'] - 273.15,2)) + " °C", font=("Helvetica", 20)), sg.Text(values[0]+"\n"+str(date.today()),size=(20,2), font=("Helvetica", 12), justification="right"), sg.Text("\n")],
            [sg.Text(w.detailed_status.title(), font=("Helvetica", 12))],
            [sg.Text("Wind: "+str(w.wind()["speed"])+" km/h")],
            [sg.Text("Humidity: "+str(w.humidity)+" %")],
            # [sg.Text(w.weather_icon_url())],
            [sg.Text(size=(30,1),font=("Helvetica", 12) , key="_timer_")],
            [sg.Button("Close")]
        ]
        # Displaying Window
        window = sg.Window('Current Weather', layout)

window.close()

