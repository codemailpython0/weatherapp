import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import requests
import os

API_KEY = '8ca3bae643c54d6daba132633250905'

class AnimatedGIF(tk.Label):
    def __init__(self, master, path, delay=100):
        im = Image.open(path)
        seq = []
        try:
            while True:
                seq.append(im.copy())
                im.seek(len(seq))  # Move to next frame
        except EOFError:
            pass

        self.frames = [ImageTk.PhotoImage(img) for img in seq]
        self.delay = delay
        self.idx = 0
        self.cancel = None
        super().__init__(master, image=self.frames[0], bg="#333333")
        self.animate()

    def animate(self):
        self.config(image=self.frames[self.idx])
        self.idx = (self.idx + 1) % len(self.frames)
        self.cancel = self.after(self.delay, self.animate)

    def stop(self):
        if self.cancel:
            self.after_cancel(self.cancel)

def get_icon_name(condition_text):
    # Basic keyword mapping for demonstration
    condition_text = condition_text.lower()
    if "sun" in condition_text or "clear" in condition_text:
        return "sunny.gif"
    elif "cloud" in condition_text:
        return "cloudy.gif"
    elif "rain" in condition_text:
        return "rain.gif"
    elif "snow" in condition_text:
        return "snow.gif"
    elif "storm" in condition_text:
        return "storm.gif"
    else:
        return "default.gif"

def get_weather():
    global anim_icon
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
            forecast_report += f"Condition: {day['day']['condition']['text']}\n\n"

        forecast_text.set(forecast_report)

        # Show animated icon
        icon_name = get_icon_name(current["condition"]["text"])
        icon_path = os.path.join("icons", icon_name)
        
        if os.path.exists(icon_path):
            if anim_icon:
                anim_icon.stop()
                anim_icon.destroy()
            anim_icon = AnimatedGIF(root, icon_path)
            anim_icon.pack(pady=10)
        else:
            print("Icon not found:", icon_path)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to get weather data.\n{e}")

# --- GUI Setup ---
root = tk.Tk()
root.title("Weather App - WeatherAPI")
root.geometry("400x500")
root.resizable(False, False)
root.configure(bg="#333333")

anim_icon = None  # To keep track of animated icon

# Entry
tk.Label(root, text="Enter City Name:", font=("Arial", 12), bg="#333333", fg="#FFFFFF").pack(pady=10)
city_entry = tk.Entry(root, font=("Arial", 14))
city_entry.pack(pady=5)

# Button
tk.Button(root, text="Get Weather", font=("Arial", 12), command=get_weather, bg="#444444", fg="#FFFFFF").pack(pady=10)

# Weather & Forecast
result_text = tk.StringVar()
forecast_text = tk.StringVar()
tk.Label(root, textvariable=result_text, font=("Arial", 12), bg="#333333", fg="#FFFFFF", justify="left", wraplength=340).pack(pady=5)
tk.Label(root, textvariable=forecast_text, font=("Arial", 12), bg="#333333", fg="#FFFFFF", justify="left", wraplength=340).pack(pady=5)

root.mainloop()
