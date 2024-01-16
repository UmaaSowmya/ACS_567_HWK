
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 16:42:33 2024

@author: puppalaumasowmya
"""

# Importing the pandas library
import pandas as pd

# Class for encapsulating data and operations related to data manipulation
class DataEncapsulation:
    def __init__(self, file_path):
        # Initialize with the file path and read existing data or create an empty DataFrame
        self.file_path = file_path
        self.data = self.read_data()

    def read_data(self):
        try:
            # Try reading data from the specified file path
            return pd.read_csv(self.file_path)
        except FileNotFoundError:
            # If the file is not found, create an empty DataFrame with specified columns
            print("File not found. Creating an empty DataFrame.")
            return pd.DataFrame(columns=["Date", "Exercise", "Duration (minutes)", "Calories burned"])

    def add_data(self, new_data):
        # Ensure that new_data has the same columns as the existing DataFrame
        if set(new_data.columns) == set(self.data.columns):
            # Concatenate the new_data to the existing DataFrame and save the updated data
            self.data = pd.concat([self.data, new_data], ignore_index=True)
            self.save_data()
            print("The data is added successfully.")
        else:
            print("Error: The columns of the new data do not match the existing data.")

    def edit_data(self, index, updated_data):
        # Ensure that updated_data has the same columns as the existing DataFrame
        if set(updated_data.columns) == set(self.data.columns):
            # Update the data at the specified index and save the changes
            self.data.loc[index] = updated_data.iloc[0]
            self.save_data()
            print("The data is edited successfully.")
        else:
            print("Error: The columns of the updated data do not match the existing data.")
            
    def delete_data(self, index):
        # Delete the data at the specified index and save the changes
        self.data = self.data.drop(index)
        self.save_data()
        print("The data is deleted successfully.")

    def save_data(self):
        # Save the current data to the specified file path
        self.data.to_csv(self.file_path, index=False)

    def calculate_mean(self):
        # Calculate and return the mean of numeric columns in the data
        numeric_columns = self.data.select_dtypes(include=['number']).columns
        return self.data[numeric_columns].mean()

    def calculate_median(self):
        # Calculate and return the median of numeric columns in the data
        numeric_columns = self.data.select_dtypes(include=['number']).columns
        return self.data[numeric_columns].median()

    def filter_data(self, filter_column, filter_value):
        try:
            # Try filtering the data based on the specified column and value
            filtered_data = self.data[self.data[filter_column] == filter_value]
            return filtered_data
        except KeyError:
            # Handle the case where the specified column does not exist
            print(f"Error: The specified column '{filter_column}' does not exist.")
        return pd.DataFrame()

# Class for managing a single instance of DataEncapsulation
class DataManagerManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Ensure that only one instance of DataManagerManager is created
        if not cls._instance:
            cls._instance = super(DataManagerManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.data_manager = None
        return cls._instance

    def initialize_data_manager(self, file_path):
        # Initialize the data manager with the specified file path
        self.data_manager = DataEncapsulation(file_path)

    def get_data_manager(self):
        # Return the instance of DataEncapsulation
        return self.data_manager

# Class for the console application, managing user interactions and options
class ConsoleApplication:
    def __init__(self):
        # Initialize the DataManagerManager and specify the file path
        self.manager = DataManagerManager()
        self.manager.initialize_data_manager("Book4.csv")

    def display_menu(self):
        # Display the menu options for the console application
        print("1. Read Data")
        print("2. Add Data")
        print("3. Edit Data")
        print("4. Delete Data")
        print("5. Data Analysis")
        print("6. Filter Data")
        print("0. Exit")

    def run(self):
        while True:
            # Display the menu and get the user's choice
            self.display_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                # Read and display the current data
                data_manager = self.manager.get_data_manager()
                print(data_manager.data)

            elif choice == "2":
                # Add new data to the existing data
                data_manager = self.manager.get_data_manager()
                new_data = pd.DataFrame({"Date": [input("Enter Date: ")],
                                         "Exercise": [input("Enter Exercise: ")],
                                         "Duration (minutes)": [int(input("Enter Duration (minutes): "))],
                                         "Calories burned": [int(input("Enter Calories burned: "))]})
                data_manager.add_data(new_data)

            elif choice == "3":
                # Edit existing data at a specified index
                data_manager = self.manager.get_data_manager()
                index = int(input("Enter the index to edit: "))
                updated_data = pd.DataFrame({"Date": [input("Enter new Date: ")],
                                             "Exercise": [input("Enter new Exercise: ")],
                                             "Duration (minutes)": [int(input("Enter new Duration (minutes): "))],
                                             "Calories burned": [int(input("Enter new Calories burned: "))]})
                data_manager.edit_data(index, updated_data)

            elif choice == "4":
                # Delete existing data at a specified index
                data_manager = self.manager.get_data_manager()
                index = int(input("Enter the index to delete: "))
                data_manager.delete_data(index)

                
            elif choice == "5":
                # Perform data analysis and display mean and median
                data_manager = self.manager.get_data_manager()
                mean_result = data_manager.calculate_mean()
                median_result = data_manager.calculate_median()
                print("Mean:")
                print(mean_result)
                print("Median:")
                print(median_result)

            elif choice == "6":
                # Filter data based on user-specified column and value
                data_manager = self.manager.get_data_manager()
                filter_column = input("Enter filter column (Date, Exercise, Duration (minutes), Calories burned): ")
                filter_value = input(f"Enter filter value for {filter_column}: ")
                filtered_data = data_manager.filter_data(filter_column, filter_value)
                print(filtered_data)

            elif choice == "0":
                # Exit the application
                break

            else:
                # Handle invalid choices
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Create an instance of ConsoleApplication and run the application
    app = ConsoleApplication()
    app.run()
