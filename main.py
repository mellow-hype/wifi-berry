# --------------------------------------------------------------------------- #
# This is the main file for the CLI interface.
# NOTE: If this script is invoked directly, the main menu will be presented.
# NOTE: To use, import this script and call the main() function.
# TODO: ...
# --------------------------------------------------------------------------- #

# Import the Menu3 module.
import menu3

# Import core/install_modes module
from wifi_berry.core.modes import automagic_install, wizard_install

def _menu_main_pre():
    """This functions contains any system/etc. actions we might need to """


def menu_main():
    """This function will run present the main menu to the user.
        TODO: Identify inputs and outputs."""

    # Call the pre-hook function, perform any intialization work needed.
    _menu_main_pre()

    # Define the variables that are needed for the menu object.
    menu_main_info_str = '[Main Menu]'
    menu_main_title_str = '[APi Setup: Main Menu] (Q to quit.)'
    menu_main_choices_l = [
        'Automagic Install',
        'Wizard Install',
        'Help'
    ]
    menu_main_prompt_str = '[Prompt]: '

    # Instantiate and configure the menu object.
    menu_main = menu3.Menu(True)
    menu_main.info(menu_main_info_str)

    # Present the menu to the user, until they exit.
    while True:
        menu_main_return = menu_main.menu(title=menu_main_title_str,
                                                choices=menu_main_choices_l,
                                                prompt=menu_main_prompt_str)

        # DEBUG: Print the return value generated by the user input.
        print(menu_main_return)

        # Create a dictionary of each selection and its corresponding function,
        # where the key is the menu choice text and the value is a function
        # pointer.
        menu_main_selections_d = {
            'Automagic Install': automagic_install,
            'Wizard Install': wizard_install,
            'Help': '',
        }

        # Access the dictionary by finding the menu choice that was selected.
        menu_main_selections_d[
            menu_main_choices_l[int(menu_main_return)-1]
        ]()

    return


# Define the main runtime function.
def main():
    """This is the main function that we will call, to initiate the menu.
        TODO: Identify inputs, and outputs [If any.]
        TODO: Scaffold child menus"""

    # Place preemptive hooks/code here.
    pass

    # Invoke the main menu.
    menu_main()

    # Perform cleanup here.
    pass

    return

# If this script is invoked directly, run the main menu.
if __name__ == '__main__':
    main()
