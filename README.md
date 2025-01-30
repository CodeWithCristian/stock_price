
# Stock Price Prediction Application

This Python application processes stock price data files, predicts the next three stock prices based on a set of rules, and outputs the results to a new file.

## Features

- **Process stock price data**: Reads CSV files with stock price data.
- **Prediction**: Predicts the next 3 stock price values using a simple algorithm based on the last 10 data points.
- **Output**: Saves the results to a new CSV file in an "output" folder.

## Requirements

- **Python 3.x**
- **Libraries**: pandas, random, heapq, logging, argparse, os

To install the necessary libraries, you can use the following command:


`pip install pandas`

## Setup and Installation

1. **Clone the Repository or Download the Script**:
    
    - Download the `stock_price_predictor.py` script to your local machine.
2. **Prepare the Input Data**:
    
    - The input data should be placed in a directory with subdirectories representing different stock exchanges.
    - Each stock exchange directory should contain CSV files formatted as follows:
        - `Stock-ID, Timestamp (dd-mm-yyyy), Stock Price`
    - Example file format:
        
        
      ```Stock-ID, Timestamp, Price
         AAPL, 01-01-2022, 150.25 
         AAPL, 02-01-2022, 152.00 
         AAPL, 03-01-2022, 151.75
         ```
        
3. **Prepare the Output Folder**:
    
    - The application will automatically create an `output` folder in the specified input directory where the processed prediction files will be saved.
    - Each output file will be named after the input file with a timestamp suffix to ensure uniqueness.

## Running the Script

### Command-Line Arguments:

- **input_folder**: Path to the root directory containing the stock exchange folders and CSV files.
- **--num_files**: (Optional) Number of files to sample per stock exchange. The default is `2`.

### Example Command:


`python stock_price_predictor.py /path/to/your/input_folder --num_files 2`

### Output:

For each file processed, a new CSV file will be created in the `output` directory with the following format:


```
Stock-ID, Timestamp, Stock Price
AAPL, 01-01-2022, 150.25
AAPL, 02-01-2022, 152.00
AAPL, 03-01-2022, 151.75
AAPL, 04-01-2022, 155.00  # Predicted value (n+1)
AAPL, 05-01-2022, 153.50  # Predicted value (n+2)
AAPL, 06-01-2022, 152.00  # Predicted value (n+3)
```

The output file will be named like:


`filename_YYYYMMDDHHMMSS_predicted.csv`

Where `YYYYMMDDHHMMSS` is the timestamp when the prediction was generated.

### Example output:

![image](https://github.com/user-attachments/assets/fa8487bf-aaa7-42db-8bdd-52fcaada5690)

## Error Handling

The application will gracefully handle the following scenarios:

- **File not found**: If a file does not exist, an error will be logged.
- **Empty files**: If a file is empty, it will be skipped, and a log will show the error.
- **Insufficient data**: If a file contains fewer than 10 valid data points, it will not be processed, and an error will be logged.

## Logs

- The application uses Python’s built-in logging module to provide feedback during execution.
- Logs will indicate the processing progress and any errors encountered.
