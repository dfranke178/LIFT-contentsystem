import pandas as pd
import os

def load_linkedin_data(csv_path='data/linkedin_posts2.csv'):
    """
    Load LinkedIn posts data from CSV file
    
    Args:
        csv_path (str): Path to the CSV file
        
    Returns:
        pandas.DataFrame: Preprocessed LinkedIn posts data
    """
    try:
        # Try a more robust approach to loading the CSV
        df = pd.read_csv(csv_path, 
                        skiprows=1,  # Skip the empty first row
                        encoding='utf-8',
                        engine='python',  # Use the python engine which is more flexible
                        error_bad_lines=False,  # Skip lines with too many fields
                        warn_bad_lines=True)    # Warn about skipped lines
        
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
                                engine='python')
            else:
                print("Could not find header row. Using default.")
        
        print(f"Final DataFrame has {len(df)} rows and {len(df.columns)} columns")
        return df
    
    except Exception as e:
        print(f"Error loading CSV: {str(e)}")
        
        # Try a very basic approach as a last resort
        print("Attempting basic file read...")
        with open(csv_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"File has {len(lines)} lines")
            print("First 3 lines:")
            for i in range(min(3, len(lines))):
                print(f"Line {i}: {lines[i][:100]}...")
        
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
            except:
                print("Could not process DATE column")
        
        # Check for engagement metrics
        engagement_cols = ['LIKES', 'COMMENTS', 'SHARES']
        for col in engagement_cols:
            if col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    print(f"Average {col.lower()}: {df[col].mean():.1f}")
                except:
                    print(f"Could not process {col} column")
        
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