#Author: Methul Welikala
#Date: 15/12/2024
#Student ID: 20231398

import tkinter as tk
import csv

first_loop = False

class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.junctions = {}  # Holds data for each junction
        self.hours = [f"{hour}:00" for hour in range(24)]  # List of hours for x-axis
        self.max_vehicles = 0  # Store max vehicles for scaling
        self.process_data()

    def process_data(self):
        """
        Processes the traffic data to accumulate the number of vehicles per hour per junction.
        """
        for row in self.traffic_data:
            junction_name = row['JunctionName']
            time = row['timeOfDay']
            hour = time.split(':')[0]  # Extract hour from the time field

            if junction_name not in self.junctions:
                self.junctions[junction_name] = [0] * 24  # Initialize 24-hour data


            hour_index = int(hour)
            self.junctions[junction_name][hour_index] += 1

        # Determine the maximum number of vehicles for scaling
        self.max_vehicles = max([max(data) for data in self.junctions.values()])

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        self.root = tk.Tk()
        self.root.title(f"Traffic Data for {self.date}")
        self.canvas = tk.Canvas(self.root, width=1800, height=600)
        self.canvas.pack()

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        bar_width = 20  # Narrower bars for grouped appearance
        colors = ["green", "red"]

        self.canvas.create_line(80, 550, 1450, 550, width=2)  # x-axis

        # Draw bars and x-axis labels in a single loop
        for i, hour in enumerate(self.hours):
            self.canvas.create_text(110 + (i * 55), 570, text=hour, angle=90)  # x-axis labels

            for j, (junction_name, data) in enumerate(self.junctions.items()):
                vehicle_count = data[i]
                if self.max_vehicles > 0:
                    bar_height = (vehicle_count / self.max_vehicles) * 500
                else:
                    bar_height = 0

                x1 = 100 + (i * 55) + (j * bar_width)
                x2 = x1 + bar_width
                y1 = 550 - bar_height

                self.canvas.create_rectangle(x1, y1, x2, 550, fill=colors[j % len(colors)], outline="black")
                self.canvas.create_text((x1 + x2) / 2, y1 - 5, text=str(vehicle_count), font=("Arial", 10, "bold"))

    def add_legend(self):
        """
        Adds a legend to the histogram.
        """
        legend_x = 1400
        legend_y = 160
        colors = ["green", "red"]

        for i, junction_name in enumerate(self.junctions):
            self.canvas.create_text(legend_x + 150, legend_y - 20, text=f"Histogram of vehicle frequency by hour ({self.date})", font=("Arial", 10, "bold"), anchor="center")
            self.canvas.create_rectangle(legend_x, legend_y + (i * 30), legend_x + 20, legend_y + (i * 30) + 20, fill=colors[i % len(colors)])
            self.canvas.create_text(legend_x + 30, legend_y + (i * 30) + 10, text=junction_name, anchor="w")

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.root.mainloop()

    def read_csv_file(file_path):
        """
        Reads the CSV file and returns the data as a list of dictionaries.
        """
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]


class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        try:
            self.current_data = HistogramApp.read_csv_file(file_path)
            print(f"Data successfully loaded from {file_path}.")
        except FileNotFoundError:
            self.current_data = None  # Reset the data to avoid showing previous file's histogram
            print(f"Error: The file '{file_path}' was not found.")
        except Exception as e:
            self.current_data = None  # Reset the data for other errors as well
            print(f"An error occurred while loading the file: {e}")

    def process_current_data(self):
        """
        Processes the currently loaded data and displays the histogram.
        """
        if not self.current_data:
            print("No data to process. Please load a CSV file first.")
            return

        date = self.current_data[0].get('Date')
        if not date:
            print("Error: 'Date' column not found in the file!")
            return

        app = HistogramApp(self.current_data, date)
        app.run()

    def process_files(self):
        """
        Handles user input for processing multiple CSV files until the user decides to quit.
        """
        def date_check(p_input, mini, maxi):
            while True:
                try:
                    value = int(input(p_input))
                except ValueError:
                    print("Integer required. Please try again.")
                else:
                    if value < mini or value > maxi:
                        print(f"Out of range - values must be in the range {mini} and {maxi}.")
                    else:
                        return value

        while True:
            day = date_check("Please enter the day of the survey in the format DD:", 1, 30)
            month = date_check("Please enter the day of the survey in the format MM: ", 1, 12)
            year = date_check("Please enter the year of the survey in the format YYYY: ", 2000, 2024)
            date = f"{day:02d}{month:02d}{year}"
            file_path = f"traffic_data{date}.csv"
            self.load_csv_file(file_path)

            if self.current_data:
                self.process_current_data()

            while True:  # Ask for Y/N confirmation
                continue_operations = input("\nDo you want to load another histogram? (Y/N): ").strip().upper()
                if continue_operations == "Y":
                    break  # Restart loop for another file
                elif continue_operations == "N":
                    print("Ending operations... Goodbye!")
                    exit()
                else:
                    print("Invalid input. Please enter 'Y' or 'N'.")


if __name__ == "__main__":
    print("****************** Welcome to the Multi-CSV Processor! *******************")
    processor = MultiCSVProcessor()
    processor.process_files()
