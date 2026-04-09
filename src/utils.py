# Import pandas for data manipulation
import pandas as pd

# Function for saving data to a CSV file, with error handling and safety checks
def save_to_csv(data, filename):
    # Safety check to ensure data is not empty before attempting to write to CSV
    if not data:
        print("No data to save. CSV file will not be created.")
        return
    
    # Convert the list of dictionaries to a DataFrame for easier CSV writing
    df = pd.DataFrame(data)

    # Save that DataFrame to a CSV file, including error handling for potential file I/O issues
    try:
        df.to_csv(filename, index=False)
    except IOError as e:
        print(f"File I/O error while saving to {filename}: {e}")

    print(f"Data successfully saved to {filename}")