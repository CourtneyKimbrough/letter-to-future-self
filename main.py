from datetime import date, timedelta
import os
import json

today = date.today()


# Function to check if date is valid
def isValidDate(dateString):
    try:
        date.fromisoformat(dateString)
        return True
    except ValueError:
        return False
    
def returnToMain ():
    # Prompt to return to the main menu
    backToMenu = input("\nWould you like to return to the main menu? (Y/N)\n")
    if backToMenu == "Y" or backToMenu == "y":
        main()
    if backToMenu == "N" or backToMenu == "n":
        quit()

# Function to create a new letter
def createLetter (file_path_os) :
    timeHeld = input("How many days would you like your letter hidden? ") # Variable to track how many days the user wants their letter hidden for
    message = input("Please enter your message:\n")
    print("Your message will be available in " + timeHeld + " days")

    # Saves file to system
    with open(file_path_os, "w") as file: 
        file.write(message)

    # Prepare data to be stored in JSON file
    letterData = {
        "file_name": file_path_os,
        "time_held": timeHeld,
        "created_date": today.isoformat()
    }

    if os.path.exists("my_dict.json"):
        with open("my_dict.json", "r") as f:
            loaded_dict = json.load(f)
    else:
        loaded_dict = [] # Creates an empty list if file does not exist 

    # Append the new letter data
    loaded_dict.append(letterData)

    # Write the updated list to the JSON file
    with open("my_dict.json", "w") as f:
        json.dump(loaded_dict, f, indent=4)

    returnToMain()


# Function to view and read letters
def viewInbox():
    if os.path.exists("my_dict.json"):
        with open("my_dict.json", "r") as f:
            loaded_dict = json.load(f)

        # Get the current date to calculate available days
        current_date = date.today()

        for letter in loaded_dict:
            # Get time letter is hidden and creation date
            time_held = int(letter["time_held"])
            created_date = date.fromisoformat(letter["created_date"])

            # Calculate available date by adding time held to created date
            available_date = created_date + timedelta(days=time_held)

            # Calculate how many days until the letter is available
            days_until_available = (available_date - current_date).days

            # Check if the letter is available now or in the future
            if days_until_available <= 0:
                print(f"\nLetter written on {letter['created_date']} is available now.\n")
            else:
                print(f"\nLetter written on {letter['created_date']} will be available in {days_until_available} days on {available_date.strftime('%Y-%m-%d')}\n")
        
        print("Enter date of letter to open or R to return to main menu")
        tryToOpen = input()
        if tryToOpen == 'R' or tryToOpen == 'r':
            main()  # Return to the main menu
        elif isValidDate(tryToOpen):
            fileToOpen = tryToOpen + ".txt"

            # Check if the entered date is associated with an available letter
            found = False
            for letter in loaded_dict:
                if letter["created_date"] == tryToOpen:
                    time_held = int(letter["time_held"])
                    created_date = date.fromisoformat(letter["created_date"])
                    available_date = created_date + timedelta(days=time_held)

                    # Ensure the letter is available
                    if available_date <= current_date:
                        found = True
                        with open(fileToOpen, "r") as f:
                            readyLetter = f.readlines()
                        print("".join(readyLetter))
                    else:
                        print(f"The letter from {tryToOpen} is not available yet. It will be available on {available_date.strftime('%Y-%m-%d')}.")
                    break
            
            if not found:
                print(f"No available letter found for the date {tryToOpen}.")
        else:
            print("Invalid date format. Please try again with the format YYYY-MM-DD.")
    else:
        print("No letters found.")
    returnToMain()

    
    
def main():  
    print("Hello! Welcome to letter for your future self. What would you like to do?\n")
    print("1. Write a new letter")
    print("2. View inbox\n")
    
    userInput = input()
    if userInput == "1":
        file_path_os = (today.isoformat() + ".txt")  # Get today's date as a string and add .txt
        if os.path.exists(file_path_os):
            print("You can only write one message per day. Please come back tomorrow.")
            returnToMain ()
        else:
            createLetter(file_path_os) # Call createLetter if file for today does not exist yet
    elif userInput == "2":
        viewInbox() # Call viewInbox is user selects option 2
        

# Call main Function
main()
