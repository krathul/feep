import argparse
import csv
import pandas as pd
import sys

def format_log_file(input_file_path, output_file_path=None):

    # Read the input CSV file and convert the Start-time column to datetime
    df = pd.read_csv(input_file_path, sep=';', header=None, names=["Start-time","Empty", "Description"])
    
    # Drop the empty column
    df.drop(columns=['Empty'], inplace=True)
    
    # Convert the Start-time column to datetime and calculate the End-time and Duration(sec) columns
    df['Start-time'] = pd.to_datetime(df['Start-time'])
    
    # Shift the Start-time column to calculate the End-time column
    df['End-time'] = df['Start-time'].shift(-1)

    # Calculate the Duration(sec) and Elapsed(sec) columns
    df['Duration(sec)'] = (df['End-time'] - df['Start-time']).dt.total_seconds()

    # Calculate the Elapsed(sec) column
    df['Elapsed(sec)'] = (df['Start-time'] - df['Start-time'].min()).dt.total_seconds()
    
    # Use csv module to write the output CSV file with the correct line endings
    csv_data = df.to_csv(sep=';', header=None, index=False, quoting=csv.QUOTE_NONNUMERIC)
    
    # Save the output CSV file or display it in the terminal
    if output_file_path:
        with open(output_file_path, 'w', newline='') as f:
            f.write(csv_data)
        print("Log file formatted successfully and saved to: " + output_file_path)
    
    # Display the output CSV file in the terminal
    else:
        sys.stdout.write(csv_data)

if __name__ == '__main__':

    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Format a log file and save it to a file or display it in the terminal.')
    parser.add_argument('input_file_path', metavar='input_file_path', type=str,
                        help='path to the input log file')
    parser.add_argument('-o', '--output_file_path', metavar='output_file_path', type=str,
                        help='path to save the formatted log file')

    # Format the log file
    args = parser.parse_args()

    # Format the log file and save it to a file or display it in the terminal 
    format_log_file(args.input_file_path, args.output_file_path)