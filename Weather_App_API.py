# Import necessary libraries
from tkinter import *             
import tkinter as tk              
import geopy                      
from geopy.geocoders import OpenCage  
from tkinter import ttk, messagebox  
from timezonefinder import TimezoneFinder  
from datetime import datetime  
import requests  
import pytz  

# Define the main function to fetch weather information
def getWeather():
    # Get the city name from the input field
    city = textfield.get()
    
    # Initialize the geolocator with OpenCage API key
    geolocator = OpenCage(api_key="a2ee88057bed425a87872c0282e75467")
    try:
        # Attempt to geocode the provided city to get its coordinates
        location = geolocator.geocode(city)
        if not location:  # If the location is not found, show an error message
            messagebox.showerror("Error", "Location not found. Please enter a valid city name.")
            return

        # Find the timezone for the given coordinates using TimezoneFinder
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
        
        if not result:  # If the timezone is not found, show an error message
            messagebox.showerror("Error", "Timezone not found for the provided location.")
            return
        
        # Get the current time in the found timezone
        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")  # Format the time (e.g., "05:49 PM")
        
        # Update the clock and current weather label in the UI
        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER: ")
        name.place(x=100, y=150)
        
        # API call to OpenWeatherMap to fetch weather information based on the city name
        api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=11d4ab6fc7a72329b878b5ba7ace8e76"
        json_data = requests.get(api).json()  # Make the HTTP GET request and parse the JSON response
        
        # Debugging: Print the JSON response to the console
        print("API Response:", json_data)
        
        # Check if the response contains the "main" key which holds weather information
        if "main" in json_data:
            # Extract weather information from the JSON response
            condition = json_data['weather'][0]['main']
            description = json_data['weather'][0]['description']
            
            # Convert temperature from Kelvin to Celsius
            temp = int(json_data['main']['temp'] - 273.15) 
            pressure = json_data['main']['pressure']
            humidity = json_data['main']['humidity']
            wind = json_data['wind']['speed']
            
            # Update the corresponding labels with the fetched weather information
            t.config(text=f"{temp} °C")
            c.config(text=f"{condition} | FEELS LIKE {temp} °C")
            w.config(text=f"{wind} m/s")
            h.config(text=f"{humidity} %")
            d.config(text=f"{description}")
            p.config(text=f"{pressure} hPa")
        
        else:
            # Show an error message if the "main" key is missing in the response
            messagebox.showerror("Error", "Weather information not found. Please try again.")
    except geopy.exc.GeocoderAuthenticationFailure as e:
        messagebox.showerror("Error", f"Authentication failure: {str(e)}. Check your API key.")
    except geopy.exc.GeocoderServiceError as e:
        messagebox.showerror("Error", f"Geocoding service error: {str(e)}")
    except geopy.exc.GeocoderTimedOut as e:
        messagebox.showerror("Error", "Request timed out. Try again later.")
    except geopy.exc.GeocoderInsufficientPrivileges:
        messagebox.showerror("Error", "Access denied. Please verify API usage.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


# Initialize the main Tkinter window (root)
root = Tk()
# Set the title of the application window
root.title("Weather API Based App")  
 # Set the window size and position on the screen
root.geometry("900x500+300+200") 
 # Prevent the window from being resized
root.resizable(False, False) 

# Create and place the search box with an image background
file_path = r"images/search.png"
Search_image = PhotoImage(file=file_path)
myimage = Label(image=Search_image)
myimage.place(x=20, y=20)

# Create the input field for the city name
textfield = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#404040", border=0, fg="white")
textfield.place(x=120, y=65)
textfield.focus()

# Create the search button with an icon
filepath_two = r"images/search_icon.png"
Search_icon = PhotoImage(file=filepath_two)
myimage_icon = Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getWeather)
myimage_icon.place(x=415, y=65)

# Create and place the weather logo image
filepath_three = r"images/logoy.png"
Logo_image = PhotoImage(file=filepath_three)
logo = Label(image=Logo_image)
logo.place(x=650, y=0)

# Create and place the bottom box image
file_path_four = r"images/box.png"
Frame_image = PhotoImage(file=file_path_four)
frame_myimage = Label(image=Frame_image)
frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

# Create and place the labels for displaying the current time and weather info
name = Label(root, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = Label(root, font=("Helvetica", 20))
clock.place(x=100, y=250)

# Create and place labels for displaying different weather parameters
label1 = Label(root, text="Wind", font=("Helvetica", 15, 'bold'), fg="white", bg='#1ab5ef')
label1.place(x=120, y=400)

label2 = Label(root, text="HUMIDITY", font=("Helvetica", 15, 'bold'), fg="white", bg='#1ab5ef')
label2.place(x=250, y=400)

label3 = Label(root, text="DESCRIPTION", font=("Helvetica", 15, 'bold'), fg="white", bg='#1ab5ef')
label3.place(x=430, y=400)

label4 = Label(root, text="PRESSURE", font=("Helvetica", 15, 'bold'), fg="white", bg='#1ab5ef')
label4.place(x=650, y=400)

# Create labels to display the actual weather data
t = Label(font=("airal", 70, "bold"), fg="#ee666d")
t.place(x=250, y=250)
c = Label(font=("airal", 15, "bold"))
c.place(x=400, y=230)
w = Label(text="...", font=("airal", 20, "bold"), bg="#1ab5ef")
w.place(x=100, y=430)
h = Label(text="...", font=("airal", 20, "bold"), bg="#1ab5ef")
h.place(x=280, y=430)
d = Label(text="...", font=("airal", 20, "bold"), bg="#1ab5ef")
d.place(x=420, y=430)
p = Label(text="...", font=("airal", 20, "bold"), bg="#1ab5ef")
p.place(x=660, y=430)

# Run the main Tkinter event loop to display the window and handle events
root.mainloop()
