from cli_radio import *

init()
while (True) :

    ##help(RadioBrowser)
    icon()
    menu()
    cmd = input("> ").strip().lower()

    if (cmd == "q") :
        clear_screen()
        break

    elif (cmd == "s") :
        print_channels()
        set_channel()
        clear_screen()

    elif (cmd == "r") :
        randomize()
        clear_screen()
        
    elif (cmd == "f") :
        select_favourite()
        clear_screen()

    elif (cmd == "sv") :
        save_channel()
        clear_screen()

    elif (cmd == "c") :
        print_countries()
        set_country()
        clear_screen()

    print()    