import os
os.environ["PATH"] = r"C:\Program Files\MPV Player" + os.pathsep + os.environ["PATH"] # Filepath for libmpv.dll

import mpv
from pyradios import RadioBrowser
import json
import random
import time


class cli_radio:
    """
    CLI Radio application using MPV media player and RadioBrowser API.

    Features:
    - Stream internet radio stations
    - Country-based browsing
    - Random station selection
    - Favorites system (JSON storage)
    - Volume control
    - Config-based startup behavior
    """

    def __init__(self):
        # Media player and API client
        self.player = mpv.MPV()
        self.rb = RadioBrowser()

        # Current playback state
        self.channel = ""
        self.country = ""
        self.region = ""

        # App state flags
        self.paused = True
        self.volume = 0
        self.stationcount = 0

        # Optional startup features
        self.icon_in_startup = False
        self.autoplay = False

        # Initialize app on startup
        self.init()

    # ----------------------------
    # Application lifecycle
    # ----------------------------

    def run(self):
        """
        Main application loop.
        Handles user input and routes commands.
        """
        while True:
            self.icon()
            self.menu()

            cmd = input("> ").strip().lower()

            if cmd == "q":
                self.clear_screen()
                exit()

            elif cmd == "s":
                self.print_channels()
                self.set_channel()
                self.clear_screen()

            elif cmd == "v":
                self.set_volume()
                self.clear_screen()

            elif cmd == "r":
                self.randomize()
                self.clear_screen()

            elif cmd == "f":
                self.select_favourite()
                self.clear_screen()

            elif cmd == "sv":
                self.save_channel()
                self.clear_screen()

            elif cmd == "c":
                self.print_countries()
                self.set_country()
                self.clear_screen()

            else:
                self.clear_screen()

    def init(self):
        """
        Loads configuration from config.json and initializes startup state.
        """
        self.clear_screen()

        try:
            with open("config.json", "r", encoding="utf-8") as file:
                config = json.load(file)

            self.channel = config["startup_channel"]
            self.region = config["startup_region"]
            self.icon_in_startup = config["startup_icon"]
            self.volume = config["startup_volume"]
            self.autoplay = config["autoplay"]

            self.channel_count()

            # Prepare initial playback
            self.play(self.channel, self.region)
            self.player.volume = self.volume

            self.paused = True

            if self.autoplay:
                self.paused = False
                self.play(self.channel, self.region)

        except json.JSONDecodeError:
            print("Config file is corrupted. Please check config.json.")
            exit()

        except IndexError:
            print("Startup channel not found in config.")
            exit()

    # ----------------------------
    # UI helpers
    # ----------------------------

    def clear_screen(self):
        """Clears terminal screen."""
        print("\033c", end="")

    def icon(self):
        """Prints startup icon if enabled in config."""
        if self.icon_in_startup:
            with open("icon.txt", "r", encoding="utf-8") as f:
                print(f.read())

    def menu(self):
        """Displays main menu and current playback state."""
        header = f"Current Region: {self.region} | Available channels: {self.stationcount}"

        print("-" * len(header))
        print(header)
        print("-" * len(header))

        print("C:  Change country")
        print("R:  Randomize")
        print("S:  Set channel")
        print("F:  Favourite channels")
        print("V:  Set volume")
        print("SV: Save current channel")
        print("Q:  Quit\n")

        print("Volume >", round(self.player.volume), "%")

        if not self.paused:
            now_playing = f"Now playing: {self.channel} | {self.country}"
            print("-" * len(now_playing))
            print(now_playing)
            print("-" * len(now_playing))

    # ----------------------------
    # Radio logic
    # ----------------------------

    def channel_count(self):
        """Updates station count for current region."""
        countries = self.rb.countries()

        for country in countries:
            if country["name"] == self.region:
                self.stationcount = country["stationcount"]
                return

    def print_channels(self):
        """Prints all stations in current region."""
        channels = self.rb.search(country=self.region)

        for i, ch in enumerate(channels, start=1):
            print(f"{i}. {ch['name']}")

        print()

    def print_countries(self):
        """Prints all available countries."""
        countries = self.rb.countries()

        for i, c in enumerate(countries, start=1):
            print(f"{i}. {c['name']}")

        print()

    def set_channel(self):
        """Allows user to select a station by name."""
        name = input("Type wanted channel > ")
        stations = self.rb.search(name=name, country=self.region)

        if not stations:
            print("No such channel!")
            time.sleep(1)
            return

        self.play(name, self.region)

    def play(self, name, region):
        """
        Plays a radio station and updates current state.
        """
        stations = self.rb.search(name=name, country=region)

        if not stations:
            print("Station not found.")
            return

        station = stations[0]

        self.player.play(station["url"])
        self.paused = False

        self.channel = station["name"]
        self.country = station["country"]

    def pause(self):
        """Pauses playback."""
        self.player.pause = True
        self.paused = True

    def randomize(self):
        """Plays a random station from a random country."""
        try:
            countries = self.rb.countries()
            country = random.choice(countries)

            stations = self.rb.search(country=country["name"])
            station = random.choice(stations)

            self.play(station["name"], country["name"])

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

    # ----------------------------
    # Settings
    # ----------------------------

    def set_volume(self):
        """Allows user to change playback volume."""
        while True:
            try:
                volume = int(input("Enter volume (0-100): "))

                if 0 <= volume <= 100:
                    self.player.volume = volume
                    return

                print("Value must be between 0 and 100.")

            except ValueError:
                print("Invalid number.")

    def set_country(self):
        """Changes current country based on user input."""
        countries = self.rb.countries()

        tmp = input("> Type country (E to exit): ").strip().lower()

        if tmp == "e":
            return

        self.region = self.find_country(tmp, countries)
        self.channel_count()

    def find_country(self, query, countries):
        """Finds matching country names based on partial input."""
        matches = [
            c["name"] for c in countries
            if query.lower() in c["name"].lower()
        ]

        if len(matches) == 1:
            return matches[0]

        if not matches:
            print("No matches found.")
            return self.region

        print("Multiple matches found:")
        for i, m in enumerate(matches, start=1):
            print(f"{i}. {m}")

        choice = input("> Select number (E to exit): ").strip().lower()

        if choice == "e":
            return self.region

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(matches):
                return matches[idx]

        print("Invalid selection")
        return self.region

    # ----------------------------
    # Favorites system
    # ----------------------------

    def select_favourite(self):
        """Loads and manages favorite stations."""
        try:
            with open("fav.json", "r", encoding="utf-8") as f:
                favorites = json.load(f)

            if isinstance(favorites, dict):
                favorites = [favorites]

            if not favorites:
                print("No saved channels")
                return

            for i, fav in enumerate(favorites, start=1):
                print(f"{i}. {fav['name']} ({fav['country']})")

            choice = input("Select number or 'rm': ")

            if choice == "rm":
                idx = int(input("Remove number: ")) - 1
                removed = favorites.pop(idx)

                with open("fav.json", "w", encoding="utf-8") as f:
                    json.dump(favorites, f, indent=4)

                print(f"Removed {removed['name']}")
                return

            if choice.isdigit():
                station = favorites[int(choice) - 1]
                self.play(station["name"], station["country"])

        except Exception:
            print("Favorites file error.")
            time.sleep(1)

    def save_channel(self):
        """Saves current station to favorites."""
        new = {
            "name": self.channel,
            "country": self.region
        }

        try:
            with open("fav.json", "r", encoding="utf-8") as f:
                favorites = json.load(f)

            if isinstance(favorites, dict):
                favorites = [favorites]

        except (FileNotFoundError, json.JSONDecodeError):
            favorites = []

        if new not in favorites:
            favorites.append(new)

        with open("fav.json", "w", encoding="utf-8") as f:
            json.dump(favorites, f, indent=4)


# ----------------------------
# Entry point
# ----------------------------

if __name__ == "__main__":
    app = cli_radio()
    app.run()