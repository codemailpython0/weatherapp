import tkinter as tk
from tkinter import messagebox
import requests
from tkinter import PhotoImage

API_KEY = '8ca3bae643c54d6daba132633250905'  # Replace with your actual WeatherAPI key

def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=3"
    
    try:
        res = requests.get(url)
        data = res.json()
        
        if "error" in data:
            messagebox.showerror("Error", f"City not found: {city}")
            return

        current = data["current"]
        location = data["location"]
        forecast = data["forecast"]["forecastday"]

        # Display current weather
        weather_report = (
            f"City: {location['name']}, {location['country']}\n"
            f"Temperature: {current['temp_c']} °C\n"
            f"Condition: {current['condition']['text']}\n"
            f"Humidity: {current['humidity']}%\n"
            f"Wind: {current['wind_kph']} kph"
        )
        result_text.set(weather_report)

        # Display forecast
        forecast_report = "3-Day Forecast:\n"
        for day in forecast:
            forecast_report += f"{day['date']} - {day['day']['maxtemp_c']}°C / {day['day']['mintemp_c']}°C\n"
            forecast_report += f"Condition: {day['day']['condition']['text']}\n"

        forecast_text.set(forecast_report)

        # Load weather icon
        icon_url = "http:" + current["condition"]["icon"]
        icon_img = PhotoImage(data=requests.get(icon_url).content)
        icon_label.config(image=icon_img)
        icon_label.image = icon_img  # Keep a reference to avoid garbage collection

    except Exception as e:
        messagebox.showerror("Error", f"Failed to get weather data.\n{e}")

# --- GUI Setup ---
root = tk.Tk()
root.title("Weather App - WeatherAPI")
root.geometry("400x400")
root.resizable(False, False)

# Dark Theme
root.configure(bg="#333333")

# Labels and Entry Widgets
tk.Label(root, text="Enter City Name:", font=("Arial", 12), bg="#333333", fg="#FFFFFF").pack(pady=10)

city_entry = tk.Entry(root, font=("Arial", 14))
city_entry.pack(pady=5)

tk.Button(root, text="Get Weather", font=("Arial", 12), command=get_weather, bg="#444444", fg="#FFFFFF").pack(pady=10)

# Weather and Forecast Results
result_text = tk.StringVar()
forecast_text = tk.StringVar()

tk.Label(root, textvariable=result_text, font=("Arial", 12), bg="#333333", fg="#FFFFFF", justify="left", wraplength=340).pack(pady=10)
tk.Label(root, textvariable=forecast_text, font=("Arial", 12), bg="#333333", fg="#FFFFFF", justify="left", wraplength=340).pack(pady=10)

# Weather Icon
icon_label = tk.Label(root, bg="#333333")
icon_label.pack(pady=10)

root.mainloop()
