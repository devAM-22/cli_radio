import os

os.environ["PATH"] = r"C:\Program Files\MPV Player" + os.pathsep + os.environ["PATH"] ##check if works on linux

##ADD VERSION CHECK OF MPV AND PYRADIOS

import mpv
from pyradios import RadioBrowser
import json
import random

player = mpv.MPV()
rb = RadioBrowser()

channel = None
region = None
icon_in_startup = None
stationcount = None
paused = True

def init() :

    clear_screen()

    global channel, region, icon_in_startup, stationcount, autoplay, channel_name, paused, channels

    try:
        with open("config.json", "r", encoding="utf-8") as file:
            config = json.load(file)

        channel = config["startup_channel"]
        region = config["startup_region"]
        icon_in_startup = config["startup_icon"]
        autoplay = config["autoplay"]

        channel_count(region)    
        channel_name = rb.search(name=channel,country=region)
    

        if (autoplay) :
            paused = False
            play(channel,region)


    except json.JSONDecodeError:
        print("Something went wrong!")
        print("Please check config.json!")
        paused = True
        exit()

    except IndexError:
        print("Could not find startup channel!")
        print("Please check config.json!")
        paused = True
        return        
    

def channel_count(region):
    global stationcount

    ##Check amount of channels in region
    countries = rb.countries()

    for i in range(len(countries)-1):
        if(countries[i]["name"] == region):
            stationcount = countries[i]["stationcount"]


def icon():
    if (icon_in_startup) :
        with open("icon.txt", "r", encoding="utf-8") as start_up:
            icon = start_up.read()
        print(icon)

def clear_screen():
    print("\033c", end="")

def menu() :


    ##Optimize stationcount
    string = "Current Region: " + region + " | Available channels: " + str(stationcount)+" |"   
    print("-"*len(string))
    print(string)
    print("-"*len(string))
    print("C:  Change country")
    print("R:  Randomize")
    print("S:  Set channel")
    print("F:  Favourite channels")
    print("SV: Save current channel") #think about cmds !
    print("Q:  Quit")
    
    if (not paused):
        playing_str = "Now playing: " + channel_name[0]["name"]+ " | " + channel_name[0]["country"] + " |"
        print("-"*len(playing_str))
        print(playing_str)
        print("-"*len(playing_str))

    

def select_favourite():
    try:
        with open("fav.json", "r", encoding="utf-8") as f:
            favorites = json.load(f)

        if isinstance(favorites, dict):
            favorites = [favorites]

        if not favorites:
            print("No saved channels")
            return

        print("List of Favourite channels:\n")

        for i, fav in enumerate(favorites, start=1):
            print(f"{i}. {fav['name']} ({fav['country']})")

        print()
        choice = input("Select channel number or 'rm' to remove: ")

        if choice == "rm":
            rm_choice = input("Enter number to remove: ")

            if not rm_choice.isdigit():
                print("Invalid input")
                return

            rm_choice = int(rm_choice)

            if rm_choice < 1 or rm_choice > len(favorites):
                print("Number out of range")
                return

            removed = favorites.pop(rm_choice - 1)

            with open("fav.json", "w", encoding="utf-8") as f:
                json.dump(favorites, f, ensure_ascii=False, indent=4)

            print(f"Removed: {removed['name']} ({removed['country']})")
            return

        if not choice.isdigit():
            print("Invalid input")
            return

        choice = int(choice)

        if choice < 1 or choice > len(favorites):
            print("Number out of range")
            return

        selected = favorites[choice - 1]
        play(selected["name"], selected["country"])

    except (FileNotFoundError, json.JSONDecodeError):
        print("No saved channels")

def save_channel():

    ##CHECK FUNCTION
    global channel_name, region

    new_favorite = {
        "name": channel_name[0]["name"],
        "country": channel_name[0]["country"]
    }

    try:
        with open("fav.json", "r", encoding="utf-8") as f:
            favorites = json.load(f)

        if isinstance(favorites, dict):
            favorites = [favorites]

    except (FileNotFoundError, json.JSONDecodeError):
        favorites = []

    for fav in favorites:
            if fav["name"] == new_favorite["name"] and fav["country"] == new_favorite["country"]:
                return
            
    favorites.append(new_favorite)

    with open("fav.json", "w", encoding="utf-8") as f:
        json.dump(favorites, f, ensure_ascii=False, indent=4)        


def print_channels() :
    global channels
    channels = rb.search(country=region) ##All channels in region + Change optimized functions (HELPs)
    for i, channel in enumerate(channels, start=1):
        print(f"{i}. {channel['name']}")

    print()

def print_countries():
    countries = rb.countries()
    for i, country in enumerate(countries, start=1):
        print(f"{i}. {country['name']}")

    print()


def set_channel():
    global region
    name = input("Type wanted channel > ")
    channels = rb.search(name=name,country=region) ##All channels in region + Change optimized functions (HELPs)
    
    if len(channels) == 0:
        print("No such channel!")
        set_channel()
    else:
        play(name,region)
    
def randomize():
    countries = rb.countries()
    country = random.choice(countries)
    channels = rb.search(country=country["name"])
    channel = random.choice(channels)
    play(channel["name"],country["name"])


def set_country():

    ##optimize
    global region, stationcount
    countries = rb.countries()

    tmp_region = input("> Type in country (E to exit): ").strip().lower()
    if tmp_region == "e":
        return None

    else:
        region = find_country(tmp_region,countries)
        channel_count(region)

def find_country(query, countries):
    global region, stationcount
    matches = [
        country["name"]
        for country in countries
        if query.lower() in country["name"].lower()
    ]

    if len(matches) == 1:
        return matches[0]

    elif len(matches) > 1:
        print("Multiple matches found:")

        for i, match in enumerate(matches, start=1):
            print(f"{i}. {match}")

        choice = input("> Select number (E to exit): ").strip().lower()

        ##Fix bugs in selection!!
        ## Check from favourite function!!

        if choice == "e":
            return

        if choice.isdigit():
            index = int(choice) - 1


            if 0 <= index < len(matches):
                return matches[index]

        else:
            print("Invalid selection")
            channel_count(region)
            return region



def play(name, region):
    global paused,channel_name
    channel_name = rb.search(name=name,country=region)
    player.play(channel_name[0]["url"])
    paused = False

def pause():
    global paused
    player.pause = True
    paused = True