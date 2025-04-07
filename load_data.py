import pandas as pd
import os
import sys

def find_csv_file(filename='linkedin_posts2.csv'):
    """Find the CSV file by checking multiple possible locations"""
    
    # List of possible locations to check
    possible_paths = [
        # Current directory
        filename,
        
        # Data subdirectory
        os.path.join('data', filename),
        
        # Parent directory
        os.path.join('..', filename),
        
        # Parent's data directory
        os.path.join('..', 'data', filename),
        
        # Absolute path if you know it
        os.path.expanduser(f"~/Documents/LIFT-contentsystem/data/{filename}")
    ]
    
    # Print current working directory for debugging
    print(f"Current working directory: {os.getcwd()}")
    
    # Check each path
    for path in possible_paths:
        print(f"Checking path: {path}")
        if os.path.exists(path):
            print(f"Found file at: {path}")
            return path
    
    # If we get here, the file wasn't found
    print(f"ERROR: Could not find {filename} in any of the checked locations")
    print("Locations checked:")
    for path in possible_paths:
        print(f"  - {path}")
    return None

def load_linkedin_data():
    """
    Load LinkedIn posts data from CSV file
    
    Returns:
        pandas.DataFrame: Preprocessed LinkedIn posts data
    """
    # First, find the CSV file
    csv_path = find_csv_file()
    
    if not csv_path:
        print("Unable to find the LinkedIn posts CSV file.")
        print("Please ensure the file exists and try again.")
        sys.exit(1)
    
    try:
        # Try a more robust approach to loading the CSV
        print(f"Attempting to load CSV from: {csv_path}")
        df = pd.read_csv(csv_path, 
                         skiprows=1,  # Skip the empty first row
                         encoding='utf-8',
                         engine='python',
                         on_bad_lines='skip')  # Skip problematic lines
        
        print(f"Successfully loaded CSV with {len(df)} rows and {len(df.columns)} columns")
        
        # Print the column names to help with debugging
        print("Column names:", df.columns.tolist())
        
        # Try a different approach if we didn't get the expected columns
        if len(df.columns) < 10:  # We expect more columns in a LinkedIn dataset
            print("Trying alternative loading method...")
            with open(csv_path, 'r', encoding='utf-8') as f:
                content = f.readlines()
            
            # Find the header row (typically row 1 or 2)
            header_row = None
            for i, line in enumerate(content[:5]):  # Check first 5 lines
                if 'POST_ID' in line or 'POST_TEXT' in line:
                    header_row = i
                    break
            
            if header_row is not None:
                print(f"Found header at line {header_row}")
                df = pd.read_csv(csv_path, 
                                skiprows=header_row,
                                encoding='utf-8', 
                                engine='python',
                                on_bad_lines='skip')
            else:
                print("Could not find header row. Using default.")
        
        print(f"Final DataFrame has {len(df)} rows and {len(df.columns)} columns")
        return df
    
    except Exception as e:
        print(f"Error loading CSV: {str(e)}")
        
        # Try a very basic approach as a last resort
        print("Attempting basic file read...")
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(f"File has {len(lines)} lines")
                print("First 3 lines:")
                for i in range(min(3, len(lines))):
                    print(f"Line {i}: {lines[i][:100]}...")
        except Exception as e2:
            print(f"Even basic file reading failed: {str(e2)}")
        
        raise e

if __name__ == "__main__":
    # Load the data
    try:
        df = load_linkedin_data()
        
        # Print basic statistics
        print(f"\nData successfully loaded!")
        print(f"Total posts: {len(df)}")
        
        # Check if DATE column exists and is properly formatted
        if 'DATE' in df.columns:
            try:
                df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
                print(f"Date range: {df['DATE'].min()} to {df['DATE'].max()}")
            except Exception as e:
                print(f"Could not process DATE column: {str(e)}")
        
        # Check for engagement metrics
        engagement_cols = ['LIKES', 'COMMENTS', 'SHARES']
        for col in engagement_cols:
            if col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    print(f"Average {col.lower()}: {df[col].mean():.1f}")
                except Exception as e:
                    print(f"Could not process {col} column: {str(e)}")
        
        # Check for topic column
        if 'TOPIC' in df.columns:
            print("\nTopic distribution:")
            topic_counts = df['TOPIC'].value_counts()
            for topic, count in topic_counts.items()[:5]:  # Show top 5 topics
                print(f"  {topic}: {count} posts")
            
        # Print a small sample of the data to verify
        print("\nSample of the data (first 2 rows):")
        print(df.head(2))
        
    except Exception as e:
        print(f"Error in main program: {str(e)}")
        print("Please check that your CSV file is properly formatted and try again.")