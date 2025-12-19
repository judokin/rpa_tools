import os
import re
from datetime import datetime

def find_latest_excel_file(directory):
    """
    Lists all excel files in the specified directory matching the pattern
    'feishu_table_data_YYYYMMDD.xlsx' and returns the path to the one with the latest date.
    """
    latest_file = None
    latest_date = None
    
    # Regex to match 'feishu_table_data_YYYYMMDD.xlsx'
    # Group 1 captures the date part
    pattern = re.compile(r"feishu_table_data_(\d{8})\.xlsx")

    try:
        for filename in os.listdir(directory):
            match = pattern.match(filename)
            if match:
                file_date_str = match.group(1)
                try:
                    file_date = datetime.strptime(file_date_str, "%Y%m%d")
                    if latest_date is None or file_date > latest_date:
                        latest_date = file_date
                        latest_file = filename
                except ValueError:
                    # Skip files with dates that don't parse correctly
                    continue
    except FileNotFoundError:
        print(f"Error: Directory not found at {directory}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    if latest_file:
        return os.path.join(directory, latest_file)
    else:
        return None

if __name__ == "__main__":
    target_directory = r"D:\data\lingxing" # Use raw string to handle backslashes
    latest_excel = find_latest_excel_file(target_directory)

    if latest_excel:
        print(f"The latest Excel file is: {latest_excel}")
    else:
        print(f"No matching Excel files found in {target_directory} or an error occurred.")
