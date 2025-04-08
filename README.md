# LIFT Content System

A system for analyzing and preparing LinkedIn post data for AI model training.

## Project Structure

```
LIFT-contentsystem/
├── src/
│   ├── data_processor.py    # Prepares training data
│   ├── analyze_data.py      # Analyzes post performance
│   ├── dashboard.py         # Interactive visualization dashboard
│   └── utils.py             # Utility functions
├── data                     # Raw LinkedIn post data
├── models/                  # Generated training data
├── analysis/                # Analysis results
└── requirements.txt         # Project dependencies
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Prepare Training Data
```bash
python src/data_processor.py
```

### 3. Run Analysis
```bash
python src/analyze_data.py
```

### 4. Launch Dashboard
```bash
streamlit run src/dashboard.py
```

## Scripts and Their Functions

### 1. Data Processing (`src/data_processor.py`)

**Purpose**: Prepares LinkedIn post data for model training.

**Function**:
- Reads raw post data from `data` file
- Processes and structures the data
- Saves formatted training data to `models/training_data.json`

**Usage**:
```bash
python src/data_processor.py
```

### 2. Data Analysis (`src/analyze_data.py`)

**Purpose**: Analyzes LinkedIn post performance and generates insights.

**Functions**:
- Analyzes post engagement metrics
- Identifies top-performing content
- Calculates success rates by content type
- Generates performance reports

**Output Files**:
- `analysis/analysis_results.json`: Complete analysis data
- `analysis/top_posts.csv`: Top 5 performing posts
- `analysis/success_rates.csv`: Success rates by content type

**Usage**:
```bash
python src/analyze_data.py
```

### 3. Dashboard (`src/dashboard.py`)

**Purpose**: Interactive visualization of LinkedIn post analysis.

**Features**:
- Overview metrics (total posts, average engagement)
- Content type distribution (pie chart)
- Success rates by content type (bar chart)
- Top performing posts with detailed metrics
- Topic analysis (top 10 topics)

**Usage**:
```bash
streamlit run src/dashboard.py
```

### 4. Utilities (`src/utils.py`)

**Purpose**: Provides helper functions for data processing and analysis.

**Key Functions**:
- `get_posts_for_training()`: Fetches and structures post data
- `save_json()`: Saves data to JSON files
- `load_json()`: Loads data from JSON files
- `create_timestamp()`: Generates formatted timestamps
- `ensure_directory()`: Creates directories if they don't exist

## Data Structure

### Training Data Format
```json
{
    "content": "Post content text",
    "metadata": {
        "post_id": "LinkedIn post URL",
        "likes": 100,
        "comments": 20,
        "shares": 5,
        "date": "2025-03-28",
        "content_type": "text-only",
        "industry": "education/learning",
        "post_length": "long",
        "purpose": "informational",
        "tone": "professional",
        "topic": "educational content",
        "cta_type": "none",
        "hashtags": "#example",
        "engagement_rate": 5.1,
        "account_size": "large",
        "success_rating": "high"
    }
}
```

## Analysis Metrics

The analysis script calculates:
- Total number of posts
- Content type distribution
- Average engagement metrics (likes, comments, shares)
- Most common topics
- Success rates by content type
- Top performing posts (based on engagement score)

## Output Files

### Analysis Results
- `analysis_results.json`: Complete analysis data
- `top_posts.csv`: Top 5 performing posts with metrics
- `success_rates.csv`: Success rates by content type

### Training Data
- `training_data.json`: Formatted data ready for model training