#Methul Binupa Welikala
#Date:11/21/2024
#Student ID:20231398

#declaring variables
Looping= True #enabling looping from start
append = False #disabling append since we havent created the file yet

# Task A: Input Validation
def validate_date_input():
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """

    def date_check(p_input, mini, maxi): #using p_input as the statement for an input
        while True:
            try:
                value = int(input(p_input)) #asking for the value with prompt p_input
            except ValueError:    #check if int
                print("Integer required. Please try again.")
            else:
                if value < mini or value > maxi:  # Check if value is out of range
                    print(f"Out of range - values must be in the range {mini} and {maxi}.") #re-printing the acceptable range
                else:
                    return value


    day = date_check("Please enter the day of the survey in the format DD:", 1, 30) #getting the input for day
    month = date_check("Please enter the day of the survey in the format MM: ", 1, 12) #getting the input for month
    year = date_check("Please enter the year of the survey in the format YYYY: ", 2000, 2024) #getting the year
    reformat_date = f"{day:02d}{month:02d}{year}"
    return(reformat_date) #returning the date


def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    answer = False #setting variable for a while loop
    while answer == False: #setting a while loop to check if user enters N
        try:
            choice = input("Do you want to load another data set? (Y/N): ").upper() #reformatting answer to uppercase
        except ValueError: #error handling for data type
            print("Enter either Y/N")
        else:
            if choice == "Y":
                print("******* loading datasets ******\n") #printing that input is valid and recieved
                answer = True
            elif choice == "N":
                print("Operations complete.....") #printing that input is valid and recieved
                answer = True
            else:
                print("Enter either Y/N only")

    return(choice) #returning the choice to quit or continue




# Task B: Processed Outcomes
def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
    sum_vehicles = 0   #variables needed to answer the questions asked
    num_trucks = 0
    num_electric = 0
    num_two_wheeled = 0
    elm_busses_north = 0
    num_no_turn = 0
    bicycle_num = 0
    speed_limit_break = 0
    hanley = 0
    elm_scooters = 0
    elm = 0
    vehicle_count_per_hour = {}
    rain = 0


    try:
        with open(f"{file_path}", "r") as file:
            file_name_write=(f"***********{file_path}***********") #qwriting file name
            data = file.readlines()[1:] #reading all lines exc3ept first line (header)

    except FileNotFoundError: #if the file name doesnt match
         print("File could not be found......")
    else:
        for i in data: #seeting up a for loop to iterate through the lists
            data_split = i.strip().split(",") #splitting lines by commas
            sum_vehicles += 1  #calculating vehichle sum
            if data_split[8] == "Truck":
                num_trucks += 1     #adding to trucks
            elif data_split[8] in ["Bicycle", "Motorcycle", "Scooter"]:
                num_two_wheeled += 1      #adding to two wheels
            if data_split[9] == "True":
                num_electric += 1    #adding to electrics
            if data_split[8] == "Buss" and data_split[0] == "Elm Avenue/Rabbit Road" and data_split[4] == 'N':
                elm_busses_north += 1     #adding to busses in elm where they go north
            if data_split[3] == data_split[4]:
                num_no_turn += 1     #adding to the vehichles going straight
            if data_split[8] == "Bicycle":
                bicycle_num += 1     #adding bicycles
            if int(data_split[7]) > int(data_split[6]):
                speed_limit_break += 1     #adding to the speed limit breaks
            if data_split[0] == "Elm Avenue/Rabbit Road":
                elm += 1  # Increment count for all vehicles in elm
                if data_split[8] == "Scooter":
                    elm_scooters += 1 #check if scooters
            if data_split[0] == 'Hanley Highway/Westway':
                hanley += 1 #adding to hanley road users
                time = data_split[2]  # getting the  time `
                hour = time.split(":")[0]  # getting the hour part of the time
                if hour not in vehicle_count_per_hour:  #if the hour is not present in the dictionary adding it as a place with count 0 so as to switch to next place
                    vehicle_count_per_hour[hour] = 0
                vehicle_count_per_hour[hour] += 1 #then  incrementing it



            if data_split[5] in ["Light Rain", "Heavy Rain"]:
                rain += 1 #adding to raining


        perc_trucks = round((num_trucks/sum_vehicles)*100)
        avg_bikes = round(bicycle_num / len(vehicle_count_per_hour))
        elm_scooters_perc = (elm_scooters * 100) // elm
        peak_vehicles_no = max(vehicle_count_per_hour.values()) #find maximum in dictionary
        peak_hours = [hour for hour,  #establish as first point
                      count in vehicle_count_per_hour.items() #check the counts
                      if count == peak_vehicles_no] #creates new list where  vehichle count is equal to peak hours
        formatted_peak_hours = [f"Between {hour}:00 and {int(hour) + 1}:00"
                                for hour in peak_hours] #format peak hours  to what is need with the second half to show the maximum peak as many times as found


        return (sum_vehicles, num_trucks, num_electric, num_two_wheeled, elm_busses_north, num_no_turn,
                bicycle_num, speed_limit_break, hanley, elm_scooters, elm,perc_trucks,avg_bikes,elm_scooters_perc,
                peak_vehicles_no,formatted_peak_hours,rain,file_name_write ) #returning all variables as a single list


def display_outcomes(values, file_found):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    try:
        output=(f'\n{values[17]}\n**************************************************\nThe total number of vehicles recorded for this date is : {values[0]}\nThe total number of trucks recorded for this date is : {values[1]}\n'
          f'The total number of electric vehicles for this date is : {values[2]}\nThe total number of two-wheeled vehicles for this date is: {values[3]}\n'
          f'The total number of Busses leaving Elm Avenue/Rabbit Road heading North is : {values[4]}\nThe total number of Vehicles through both junctions not turning left or right is: {values[5]}\n'
          f'The percentage of total vehicles recorded that are trucks for this date is: {values[11]}%\nthe average number of Bikes per hour for this date is: {values[12]}\n'
          f'The total number of Vehicles recorded as over the speed limit for this date is : {values[7]}\nThe total number of vehicles recorded through Elm Avenue/Rabbit Road junction is: {values[10]}\n'
          f'The total number of vehicles recorded through Hanley Highway/Westway junction is : {values[8]}\n{values[13]}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.\n'
          f'The highest number of vehicles in an hour on Hanley Highway/Westway is: {values[14]}\nThe most vehicles through Hanley Highway/Westway were recorded between: {values[15]}\n'
          f'The number of hours of rain for this date is: {values[16]}\n**************************************************\n\n') #prinitng all the results
    except:
        pass
    else:
        print(output)
        return (output) #returning the output to print it in a text file


# Task C: Save Results to Text File
def save_results_to_file(output, file_name, append_status):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    if append_status == False:  # checking  if recieved parameter is to not append
        try:
            with open(file_name, "w") as file:
                if output:  # Check if output is not None or empty
                    file.write(output)  # Write the output to the file
                    file.write("\n")  # Add a newline for readability
        except FileNotFoundError:
                print(" ", end ="")

    else:
        try:
            with open(file_name, "a") as file:
                if output:  # Check if output is not None or empty
                    file.write(output)  # Write the output to the file
                    file.write("\n")  # Add a newline for readability
                else:
                    print("", end = " ")

        except FileNotFoundError:
            print(" ", end ="")







while Looping == True:
    date = validate_date_input()
    file_path = f"traffic_data{date}.csv" #determining file name
    values = process_csv_data(file_path) #sending the correct file name to the process function

    output= display_outcomes(values, file_path) #getting the output to write to the txt file
    if append == False: #determining if needed to append  or write
        save_results_to_file(output,"results.txt", False)  #sending needed parameters to function
    else:
        save_results_to_file(output, "results.txt", True)
    status = validate_continue_input() #getting the output to continue or stop
    if status == "N":
        Looping = False #stoipping the looping
    else:
        append = True #enabling appending since writing has been done once
