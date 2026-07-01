"""
Weather App Desktop App
Built with Tkinter (built-in) + requests

Uses Open-Meteo (https://open-meteo.com) - a completely free weather API
that requires NO API key and NO signup.

Install the one extra dependency before running:
    pip install requests
"""

import tkinter as tk
from tkinter import messagebox
import requests
import threading

# Maps Open-Meteo's numeric weather codes to human-readable descriptions
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    56: "Light freezing drizzle", 57: "Dense freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    66: "Light freezing rain", 67: "Heavy freezing rain",
    71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",
}


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("400x480")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")

        # --- Title ---
        title_label = tk.Label(
            root, text="Weather App", font=("Helvetica", 20, "bold"),
            bg="#2c3e50", fg="white"
        )
        title_label.pack(pady=15)

        # --- Search bar ---
        search_frame = tk.Frame(root, bg="#2c3e50")
        search_frame.pack(pady=5)

        self.city_entry = tk.Entry(search_frame, width=24, font=("Helvetica", 12))
        self.city_entry.pack(side=tk.LEFT, padx=5)
        self.city_entry.insert(0, "Lagos")
        self.city_entry.bind("<Return>", lambda event: self.search_weather())

        search_btn = tk.Button(
            search_frame, text="Search", bg="#3498db", fg="white",
            font=("Helvetica", 10, "bold"), command=self.search_weather
        )
        search_btn.pack(side=tk.LEFT)

        # --- Status / loading label ---
        self.status_label = tk.Label(
            root, text="", font=("Helvetica", 9), bg="#2c3e50", fg="#95a5a6"
        )
        self.status_label.pack(pady=5)

        # --- Result card ---
        card = tk.Frame(root, bg="#34495e", padx=20, pady=20)
        card.pack(pady=15, padx=30, fill="both", expand=True)

        self.location_label = tk.Label(
            card, text="—", font=("Helvetica", 15, "bold"),
            bg="#34495e", fg="white", wraplength=300
        )
        self.location_label.pack(pady=(0, 10))

        self.temp_label = tk.Label(
            card, text="—", font=("Helvetica", 42, "bold"),
            bg="#34495e", fg="#ecf0f1"
        )
        self.temp_label.pack()

        self.condition_label = tk.Label(
            card, text="", font=("Helvetica", 13),
            bg="#34495e", fg="#bdc3c7"
        )
        self.condition_label.pack(pady=(0, 15))

        details_frame = tk.Frame(card, bg="#34495e")
        details_frame.pack(fill="x")

        self.feels_like_label = tk.Label(
            details_frame, text="", font=("Helvetica", 10),
            bg="#34495e", fg="#bdc3c7", justify="left", anchor="w"
        )
        self.feels_like_label.pack(fill="x")

        self.humidity_label = tk.Label(
            details_frame, text="", font=("Helvetica", 10),
            bg="#34495e", fg="#bdc3c7", justify="left", anchor="w"
        )
        self.humidity_label.pack(fill="x")

        self.wind_label = tk.Label(
            details_frame, text="", font=("Helvetica", 10),
            bg="#34495e", fg="#bdc3c7", justify="left", anchor="w"
        )
        self.wind_label.pack(fill="x")

        # Load a default city on startup
        self.search_weather()

    def search_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Empty Field", "Please enter a city name.")
            return

        self.status_label.config(text="Loading...")
        self.root.update_idletasks()

        # Run the network call in a background thread so the UI doesn't freeze
        threading.Thread(target=self.fetch_weather, args=(city,), daemon=True).start()

    def fetch_weather(self, city):
        try:
            # Step 1: convert city name -> latitude/longitude (free, no key needed)
            geo_url = "https://geocoding-api.open-meteo.com/v1/search"
            geo_params = {"name": city, "count": 1, "language": "en", "format": "json"}
            geo_resp = requests.get(geo_url, params=geo_params, timeout=10)
            geo_data = geo_resp.json()

            if not geo_data.get("results"):
                self.root.after(0, self.show_error, f"City '{city}' not found.")
                return

            place = geo_data["results"][0]
            lat, lon = place["latitude"], place["longitude"]
            place_name = place.get("name", city)
            country = place.get("country", "")
            admin1 = place.get("admin1", "")
            location_str = ", ".join(filter(None, [place_name, admin1, country]))

            # Step 2: fetch current weather for those coordinates
            weather_url = "https://api.open-meteo.com/v1/forecast"
            weather_params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,"
                           "weather_code,wind_speed_10m",
                "timezone": "auto",
            }
            weather_resp = requests.get(weather_url, params=weather_params, timeout=10)
            weather_data = weather_resp.json()

            current = weather_data["current"]

            self.root.after(0, self.display_weather, location_str, current)

        except requests.exceptions.RequestException:
            self.root.after(0, self.show_error, "Network error. Check your internet connection.")
        except (KeyError, IndexError, ValueError):
            self.root.after(0, self.show_error, "Couldn't read weather data. Try again.")

    def display_weather(self, location_str, current):
        self.status_label.config(text="")
        self.location_label.config(text=location_str)

        temp = current.get("temperature_2m")
        feels_like = current.get("apparent_temperature")
        humidity = current.get("relative_humidity_2m")
        wind = current.get("wind_speed_10m")
        code = current.get("weather_code")

        condition = WEATHER_CODES.get(code, "Unknown")

        self.temp_label.config(text=f"{temp:.0f}°C")
        self.condition_label.config(text=condition)
        self.feels_like_label.config(text=f"Feels like: {feels_like:.0f}°C")
        self.humidity_label.config(text=f"Humidity: {humidity:.0f}%")
        self.wind_label.config(text=f"Wind speed: {wind:.0f} km/h")

    def show_error(self, message):
        self.status_label.config(text="")
        messagebox.showerror("Error", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
