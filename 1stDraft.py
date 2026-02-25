import time, io, os 

def cap(string): #Capitalises any proper nouns, to keep the formatting consistent no matter the input
    if string != "":
        string = string[0].upper + string[1:].lower
    return string

def find(name): #Simple linear search which returns the position, or -1 if it is not contained within the array
    global names
    if name in names: 
        for x in range(len(names)):
            if names[x] == name: 
                return x
    else:  
        return -1

def search(array, type, parameter): #Narrows down an array based on specific parameters:
    result = [] 
    match type:
        case "type": #If the parameter given is for type
            for x in range(len(array)):
                if array[x][3] == parameter or array[x][4] == parameter:
                    result.append(array[x]) 
        case "health": #If the parameter given is for health
            for x in range(len(array)): #If the health difference is less than 20%, the difference is saved in the final place 
                num = abs(array[x][2] - parameter)
                if num <= parameter // 5:
                    array[x].append(num)
                    result.append(array[x]) 
            sorted = False 
            while sorted == False: #Bubblesort using the final place, which was added in the last step
                sorted = True
                for x in range(len(result) - 1): 
                    if result[x][len(result)] > result[x+1][len(result)]:
                        temp = result[x][len(result)]
                        result[x][len(result)] = result[x+1][len(result)] 
                        result[x+1][len(result)] = temp
                        sorted = False 
            for x in range(len(result)):
                result[x] = result[x][:len(result) - 1] 
        case "evolution": #If the parameter given is the name of an evolution
            for x in range(len(array)):
                for i in range(6, array[x][5]):
                    if array[x][i].lower() == parameter.lower(): 
                        result.append(array[x])
                        break   
        case "move": #If the parameter given is the name of a move 
            for x in range(len(array)):
                cur = array[array[5]:] 
                for i in range(0, len(cur), 4): #This steps by 4, as each move has 4 attributes (name, damage, type, additional information) 
                    if cur[i] == parameter:
                        result.append(array[x])
                        break  
    #No case _: is required because this variable is assigned by the program itself, so there cannot be errors.      
    return result

def display_entry(name): #Shows the Pokédex entry of a specific Pokémon
    global names, entries 
    position = find(name) #Finds the position of the Pokémon
    print("Name: ", names[position])
    time.sleep(0.1)  
    print("Pokédex no. : ", entries[position][0])
    time.sleep(0.1) 
    print("Description: ", entries[position][1])
    time.sleep(0.1) 
    print("Health: ", entries[position][2])
    time.sleep(0.1) 
    print("Primary type: ", entries[position][3])
    time.sleep(0.1)  
    if entries[position][4] != "": #If the Pokémon has 2 types
        print("Secondary type: ", entries[position][4])
        time.sleep(0.1)  
    num = entries[position][5] #This stores the location of the last evolution, as Pokémon can have as little as 0 and as much as 7
    temp = []
    for x in range(6, num):
        temp.append(entries[position][x])
    if temp != []: 
        evo = ", ".join(temp)
        print(f"Evolutions: {evo}")
        time.sleep(0.1)  
    cur = entries[position][num:] 
    for x in range(0, len(cur), 4): #For all the moves, as the amount that are stored is variable
        print(f"Move {x+1}'s name: {cur[x]}")
        time.sleep(0.1) 
        print(f"Move {x+1}'s damage: {cur[x+1]}")
        time.sleep(0.1) 
        if cur[x+2] != "":
            print(f"Move {x+1}'s additional information: {cur[x+2]}")
            time.sleep(0.1) 

def add_new(): 
    global names, entries
    name = input("What is the name of the Pokémon: ") #Gathering data 
    name = cap(name)
    time.sleep(0.1)   
    names.append(name) 
    cur = [] 
    cur.append(input(f"What is {name}'s Pokédex number: ")) 
    time.sleep(0.1)  
    cur.append(input(f"Give a short description for {name}: "))
    time.sleep(0.1)  
    cur.append(input(f"What is {name}'s health: "))
    time.sleep(0.1)   
    cur.append(cap(input(f"What is {name}'s primary type: ")))
    time.sleep(0.1)   
    cur.append(cap(input(f"What is {name}'s secondary type (Press enter if not applicable):")))
    time.sleep(0.1) 
    ans = input(f"Does {name} have any evolutions (higher or lower)? (y/n): ").lower()
    cur.append(6) 
    x = 0 
    while ans == "y": #While the Pokémon still has moves left
        evo = input(f"What is the name of {name}'s evolution?: ") 
        cur.append(cap(evo))
        ans = input(f"Does {name} have any more evolutions? (y/n): ").lower() 
        x += 1
    cur[5] += x
    for x in range(len(names)): #This loop ensures that the evolutions are consistent e.g. if you add a Pokémon which evolves into Gardevoir, Gardevoir's entry will always contain this Pokémon under evolutions. 
        if names[x] in cur[6:cur[5]]:
            if cur[0] not in entries[x][6:entries[x][5]]:
                entries[x] = entries[x][:entries[x][5]] + cur[0] + entries[[x][5] + 1:]
                entries[x][5] += 1  
    ans = input(f"Would you like to add any moves for {name}? (y/n):") 
    ans = ans.lower()   
    while ans != "n": 
        cur.append(cap(input(f"What is {name}'s next move: "))) 
        cur.append(input(f"What is the damage of this move: ")) 
        cur.append(input(f"Any additional information: ")) 
        ans = input(f"Would you like to add any moves for {name}? (y/n):") 
    entries.append(cur) 
    display_entry(name) #Visual check
    ans = input("Is this information correct? (y/n): ") 
    ans = ans.lower()
    if ans == "n": 
        edit_entry(name)  
     
def edit_entry(name):
    global names, entries 
    if name == "": #If the function was not called from the add_entry() function
        name = input("What Pokémon's entry would you like to edit: ") 
        pos = find(name) 
        while pos == -1: 
            name = input("Sorry, that didn't work. Could you re-enter the name?: ")
            pos = find(name) 
    display_entry(name) 
    bool = True 
    while bool == True: #Until the user says they have nothing more to change
        move = False  
        print("What attribute would you like to change?") #Secondary menu
        time.sleep(0.1) 
        print("1. Name") 
        time.sleep(0.1) 
        print("2. Health") 
        time.sleep(0.1) 
        print("3. Pokédex no." )
        time.sleep(0.1) 
        print("4. Pokédex entry") 
        time.sleep(0.1) 
        print("5. Primary type")
        time.sleep(0.1)  
        print("6. Secondary type (If applicable)")
        time.sleep(0.1) 
        print("7. Evolutions")
        time.sleep(0.1)  
        print("8. Moves") 
        ans = input()
        match ans:  
            case "1":  
                names[pos] = input("What would you like to change {name}'s name to: ")
            case "2": 
                entries[pos][2] = input("What would you like to change {name}'s health to: ") 
            case "3": 
                entries[pos][0] = input("What would you like to change {name}'s Pokédex no. to: ") 
            case "4":   
                entries[pos][1] = input("What would you like to change {name}'s Pokédex entry to: ")
            case "5": 
                entries[pos][3] = input("What would you like to change {name}'s primary type to: ")
            case "6": 
                entries[pos][4] = input("What would you like to change {name}'s secondary type to: ")
            case "7": 
                no = int(input(f"Which of {name}'s evolutions would you like to change (give a number): ")) 
                no += 5 
                entries[pos][no] = input("What would you like to change the evolution's name to?: ") 
            case "8": 
                move = True
            case _: 
                print("Sorry, that didn't work. Please try again") 
        if move: #If they are editing a move
            num = int(input("Which move would you like to change? (Give a number): ")) 
            num -= 1 
            num1 = entries[pos][5] + (3 * num)
        while move: #Until the user is done entering 
            print("Would you like to change the move's") #Secondary menu
            print("1. Name") 
            print("2. Damage")
            print("3. Type")
            print("4. Additional information") 
            ans = input() 
            match ans: 
                case "1": 
                    entries[num1] = input("What would you like the new name to be: ") 
                case "2": 
                    entries[num1+1] = input("What would you like the new damage to be: ") 
                case "3":
                    entries[num1+3] = input("What would you like the new type to be: ")
                case "4": 
                    entries[num1+2] = input("What would you like the new additional information to be: ")
                case _: 
                    print("Sorry, that didn't work")  
            ans = input("Would you like to edit anything more about this move? (y/n): ") 
            ans = ans.lower()
            if ans == "n":
                move = False 
        ans = input("Would you like to edit anything more about this Pokémon? (y/n): ") 
        ans = ans.lower()
        if ans == "n":
            bool = False     

def search_for_pokemon():
    global entries, names  
    array = entries #Array of all the results
    for x in range(len(array)): #Consolidates the names with the entries
        array[x].append(names[x])
    ans = input("Do you know the name of this Pokémon? (y/n): ").lower() 
    if ans == "y": 
        name = input("What is the Pokémon's name?: ")
        display_entry(name) 
    else: 
        ans = "y"
        while ans == "y": #Until the user is done entering attributes
            ans = "y" 
            parameter = ""
            print("What attributes do you know?: ")
            print("1. Approximate health") 
            print("2. Any evolutions (higher or lower)")
            print("3. Either type of the Pokémon")
            print("4. Moves") 
            print("5. Search")
            ans = input() 
            match ans:
                case "1":
                    parameter = int(input("What is the approximate health?: "))
                    type = "health" 
                case "2":
                    parameter = input("What is the evolution's name?: ")
                    type = "evolution" 
                case "3":
                    parameter = input("What is the type that you know?: ") 
                    type = "type"
                case "4": 
                    parameter = input("What is the move's name?: ")
                    type = "move"
                case "5":
                    array = [array[x][len(array[x])] for x in range(len(array))] 
                    num = input(f"How many results would you like (up to {len(array)}): ") 
                    num -= 1 
                    for x in range(num):
                        display_entry(array[x])
                case _:
                    print("Sorry, that didn't work. Could you please try again") 
            if type != "":
                array = search(array, type, parameter)
 
def load_file(): #Loads the data from a specific file
    global names, entries
    bool = True
    while bool:
        file = input("What file would you like to load?: ") 
        if ".txt" in file: 
            bool = False
            if os.path.exists(file):
                try: 
                    f = open(file, "r") #Opens file for read
                    temp = f.read()
                    lines = temp.split("\n") #Breaks the file into lines (entries)
                    f.close() #Closes the file
                except:
                    print("Sorry, that file cannot be written to. Could you enter another filename?")
                    bool = True
            else: 
                print("Sorry, that file does not exist. Could you enter another filename?")
        else: 
            print("Sorry, that file is not in the .txt format. Could you enter another filename?")

def save_file(): #Copies the data to a specific file
    bool = True
    save = []
    for x in range(len(names)): #This function formats the data 
        temp = [names[x], "/"]
        for i in range(len(entries[x])):
            temp.append(entries[x][i], "/") 
        save.append(temp)  
    while bool:
        file = input("What filename would you like it to be saved under?: ") 
        if ".txt" in file: #The file is given in the correct
            bool = False
            try: #I'm only using this because as far as I know, there is no way to preemptively tell if a file can be written to (Is in the same directory as the code).
                if os.path.exists(file):
                    f = open(file, "w") #Opens the file for write
                    f.write("\n".join(save)) #Adds linebreaks between every entry
                    f.close() #Closes the file
                else: 
                    f = open(file, "x") #This creates a new file
                    f.close()
                    f = open(file, "w") 
                    f.write("\n".join(save)) 
                    f.close()
            except:
                print("Sorry, that file cannot be written to. Could you enter another filename?") #If the file is in a different directory
                bool = True
        else: 
            print("Sorry, that file is not in the .txt format. Could you enter another filename?") #Self explanatory            

def file_handling():
    bool = False 
    while not bool: #Until a valid input has been given
        print("What would you like to do: ") #Secondary menu
        print("1. Load Pokédex from file") 
        print("2. Save current Pokédex to file")
        print("3. Cancel") 
        ans = str(input())
        match ans: #Case statement for handling the input
            case "1":
                load_file() 
                bool = True 
            case "2":
                save_file()
                bool = True
            case "3": 
                bool = True 
            case _: 
                print("Sorry, that didn't work. Could you please try again?")

# Initialisations
names = []
entries = [] 
ans = 0
quit = False

# Main loop  
while not quit:
    print("What would you like to do?") #Menu
    time.sleep(0.1) 
    print("1. Add new Pokémon")  
    time.sleep(0.1) 
    print("2. Edit the entry of an already existing Pokémon") 
    time.sleep(0.1)
    print("3. Search for a Pokeémon or multiple Pokémon") 
    time.sleep(0.1) 
    print("4. Save to or load from file") 
    time.sleep(0.1) 
    print("5. Quit") 
    
    ans = input() 
    
    match ans: #Case statement for the input
        case "1": 
            add_new() 
        case "2": 
            edit_entry("") 
        case "3": 
            search_for_pokemon() 
        case "4":
            file_handling() 
        case "5":
            print("Bye bye 👋") 
            quit = True 
        case _: #This handles any other inputs. 
            print("Sorry, that didn't work.")
