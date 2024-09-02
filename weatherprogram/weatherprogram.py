import requests 
from PIL import Image, ImageTk
import tkinter as tk 
from tkinter import messagebox
import os

def get_weather(api_key, country, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "main" in data and "weather" in data:
            weather_info = (
                f"*** Weather in {city}, {country} ***\n"
                f"Temperature: {data['main']['temp']}°C\n"
                f"Feels like: {data['main']['feels_like']}°C\n"
                f"Humidity: {data['main']['humidity']}%\n"
                f"Weather: {data['weather'][0]['main']}\n"
                f"Wind Speed: {data['wind']['speed']}m/s"
            )
            display_weather(weather_info, data['weather'][0]['main'].lower())
        else:
            messagebox.showerror("Error", "City not found or invalid response!")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")
        
def display_weather(info, condition):
    for widget in weather_frame.winfo_children():
        widget.destroy()
        
    label = tk.Label(weather_frame, text=info, bg="#2e2e2e", fg="white", font=("Helvetica", 12), justify=tk.LEFT, wraplength=250)
    label.pack(side=tk.LEFT, padx = 10, pady = 10)
    show_weather_image(condition)

def show_weather_image(condition):
    img_file={
        'clear': 'sun.png', 'clouds': 'clouds.png', 'rain': 'rain.png',
        'snow': 'snow.png', 'thunderstorm': 'thunderstorm.png',
        'drizzle': "drizzle.png", 'wind': 'wind.png',
    }.get(condition,'default.png')
    
    img_path = os.path.join('images', img_file)
    if os.path.exists(img_path):
        img = ImageTk.PhotoImage(Image.open(img_path).resize((80, 80), Image.LANCZOS))
        img_label = tk.Label(weather_frame, image = img, bg = "#2e2e2e")
        img_label.image = img
        img_label.pack(side=tk.RIGHT, padx = 10, pady = 10)

def fetch_weather():
    country = country_entry.get().strip()
    city = city_entry.get().strip()
    
    if country and city:
        get_weather(api_key, country, city)
    else:
        messagebox.showwarning("input Error", "Please enter both country and city.")
        
root = tk.Tk()
root.title("Weather App")
root.geometry("400x350")
root.configure(bg ="#1e1e1e")


api_key = 'f4710ff506f714b419535360dea9c1d0'

tk.Label(root, text="Country Code: ", bg="#1e1e1e", fg="white").pack(pady=5)
country_entry = tk.Entry(root)
country_entry.pack(pady=5)

tk.Label(root, text = "City name: ", bg="#1e1e1e", fg="white").pack(pady=5)
city_entry = tk.Entry(root)
city_entry.pack(pady=5)

tk.Button(root, text="Get Weather: " , command=fetch_weather, bg="#3e3e3e", fg="white").pack(pady=10)

weather_frame = tk.Frame(root, bg="#2e2e2e", bd=2, relief=tk.SUNKEN) 
weather_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()  