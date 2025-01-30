import pandas as pd
import random
import heapq
import logging
from datetime import datetime, timedelta
import os
import argparse

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_csv_files(directory, num_files_to_sample):
    try:
        # Ensure we do not process the 'output' directory
        if 'output' in directory:
            logging.info(f"Skipping output directory: {directory}")
            return []
        
        files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
        random.shuffle(files)
        return files[:min(num_files_to_sample, len(files))]
    except Exception as e:
        logging.error(f"Error fetching files from {directory}: {e}")
        return []


def get_10_consecutive_points(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        df = pd.read_csv(file_path, header=None, names=['Stock-ID', 'Timestamp', 'Price'])
        
        if df.empty:
            raise ValueError(f"File is empty: {file_path}")
        
        # Ensure proper conversion of Timestamp and Price columns
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d-%m-%Y', errors='coerce')  # Adjusted for DD-MM-YYYY format
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        
        # Remove rows where Timestamp or Price is missing
        df.dropna(subset=['Timestamp', 'Price'], inplace=True)
        
        df = df.sort_values(by='Timestamp')
        
        if len(df) < 10:
            raise ValueError(f"Not enough data points in file: {file_path}. Need at least 10, found {len(df)}")
        
        start_index = random.randint(0, len(df) - 10 - 1)
        consecutive_points = df.iloc[start_index:start_index + 10]
        
        return consecutive_points
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")
        return None


def predict_next_3_values(consecutive_points):
    try:
        if consecutive_points is None or len(consecutive_points) != 10:
            raise ValueError("Invalid input: Expected 10 consecutive data points")
        
        prices = consecutive_points['Price'].tolist()
        second_highest = heapq.nlargest(2, prices)[1]
        
        n_plus_1 = second_highest
        n_plus_2 = n_plus_1 + (n_plus_1 - prices[-1]) / 2
        n_plus_3 = n_plus_2 + (n_plus_2 - n_plus_1) / 4
        
        last_timestamp = consecutive_points['Timestamp'].iloc[-1]
        
        predicted_points = [
            (consecutive_points['Stock-ID'].iloc[0], last_timestamp + timedelta(days=1), n_plus_1),
            (consecutive_points['Stock-ID'].iloc[0], last_timestamp + timedelta(days=2), n_plus_2),
            (consecutive_points['Stock-ID'].iloc[0], last_timestamp + timedelta(days=3), n_plus_3)
        ]
        
        return predicted_points
    except Exception as e:
        logging.error(f"Error predicting values: {e}")
        return None

def process_files(base_directory, num_files_to_sample):
    try:
        output_directory = os.path.join(base_directory, "output")
        os.makedirs(output_directory, exist_ok=True)
        
        exchanges = [d for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]
        
        for exchange in exchanges:
            exchange_dir = os.path.join(base_directory, exchange)
            if not os.path.exists(exchange_dir):
                logging.warning(f"Directory not found: {exchange_dir}, skipping.")
                continue
            
            file_paths = get_csv_files(exchange_dir, num_files_to_sample)
            
            for file_path in file_paths:
                consecutive_points = get_10_consecutive_points(file_path)
                
                if consecutive_points is not None:
                    predicted_points = predict_next_3_values(consecutive_points)
                    
                    if predicted_points is not None:
                        all_points = consecutive_points.values.tolist() + predicted_points
                        output_df = pd.DataFrame(all_points, columns=['Stock-ID', 'Timestamp', 'Price'])
                        
                        output_file_name = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(file_path))[0]}_{datetime.now().strftime('%Y%m%d%H%M%S')}_predicted.csv")

                        output_df.to_csv(output_file_name, index=False)
                        
                        logging.info(f"Output saved to {output_file_name}")
    except Exception as e:
        logging.error(f"Error processing files: {e}")

def main():
    try:
        setup_logging()
        parser = argparse.ArgumentParser(description="Stock price prediction script.")
        parser.add_argument("input_folder", type=str, help="Path to the stock data directory")
        parser.add_argument("--num_files", type=int, default=2, help="Number of files to sample per exchange (default: 2)")
        
        args = parser.parse_args()
        
        process_files(args.input_folder, args.num_files)
    except Exception as e:
        logging.error(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
