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
    # Load the CSV file
    df = pd.read_csv(csv_path, skiprows=1)  # Skip the empty first row
    
    # Rename columns if needed (adjust based on your CSV structure)
    df.columns = [
        "POST_ID", "POST_TEXT", "LIKES", "COMMENTS", "SHARES", 
        "DATE", "CONTENT_TYPE", "INDUSTRY", "POST_LENGTH", 
        "PURPOSE", "TONE", "TOPIC", "CTA_TYPE", "HASHTAGS", 
        "ENGAGEMENT_RATE", "ACCOUNT_SIZE", "SUCCESS_RATING"
    ]
    
    # Clean the data
    df = df[~df['POST_ID'].str.contains('POST_ID', na=False)]  # Remove header row if it was included
    
    # Convert numeric columns
    numeric_cols = ['LIKES', 'COMMENTS', 'SHARES', 'ENGAGEMENT_RATE']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Convert date column
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    
    # Calculate additional features if needed
    df['TOTAL_ENGAGEMENT'] = df['LIKES'] + df['COMMENTS'] + df['SHARES']
    
    return df

if __name__ == "__main__":
    # Load the data
    df = load_linkedin_data()
    
    # Print basic statistics
    print(f"Total posts: {len(df)}")
    print(f"Date range: {df['DATE'].min()} to {df['DATE'].max()}")
    print(f"Average engagement: {df['LIKES'].mean():.1f} likes, {df['COMMENTS'].mean():.1f} comments, {df['SHARES'].mean():.1f} shares")
    
    # Print topic distribution
    print("\nTopic distribution:")
    topic_counts = df['TOPIC'].value_counts()
    for topic, count in topic_counts.items():
        print(f"  {topic}: {count} posts")
    
    # Print a sample post
    print("\nSample post:")
    sample = df.sample(1).iloc[0]
    print(f"Topic: {sample['TOPIC']}")
    print(f"Engagement: {sample['LIKES']} likes, {sample['COMMENTS']} comments, {sample['SHARES']} shares")
    print(f"Text preview: {sample['POST_TEXT'][:150]}...")