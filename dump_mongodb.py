import os
import json
import time
from dotenv import load_dotenv
from pymongo import MongoClient

def dump_collection_to_json():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get MongoDB connection parameters from environment variables
    mongo_uri = os.getenv('MONGO_URI')
    db_name = os.getenv('MONGO_DB_NAME')
    collection_name = os.getenv('MONGO_COLLECTION_NAME')
    
    # Check if all required parameters are present
    if not all([mongo_uri, db_name, collection_name]):
        raise ValueError("Missing required environment variables: MONGO_URI, MONGO_DB_NAME, and MONGO_COLLECTION_NAME must be set")
    
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    
    # Get total document count for progress calculation
    total_documents = collection.count_documents({})
    print(f"Found {total_documents} documents in collection")
    
    # Initialize progress tracking
    start_time = time.time()
    last_update_time = start_time
    processed = 0
    
    # Create file for output
    output_file = 'news_backup.json'
    
    # Batch processing for large datasets
    batch_size = 10000  # Process in batches to reduce memory usage
    data = []
    
    # Process documents in batches
    cursor = collection.find()
    for doc in cursor:
        doc.pop('_id', None)  # Remove the _id field as it can cause issues when re-importing
        data.append(doc)
        processed += 1
        
        # Update progress every 1000 documents or every 5 seconds
        if processed % 1000 == 0 or time.time() - last_update_time >= 5:
            last_update_time = time.time()
            
            # Calculate progress percentage
            progress = (processed / total_documents) * 100 if total_documents > 0 else 100
            
            # Create progress bar
            bar_length = 50
            filled_length = int(bar_length * processed // total_documents) if total_documents > 0 else bar_length
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            
            # Display progress
            print(f"\rProgress: |{bar}| {progress:.2f}% ({processed}/{total_documents} documents processed)", end='')
            
            # Write batch to file periodically to reduce memory usage
            if len(data) >= batch_size:
                with open(output_file, 'a') as f:
                    json.dump(data, f, indent=2)
                data = []
    
    # Write any remaining documents in the last batch
    if data:
        with open(output_file, 'a') as f:
            json.dump(data, f, indent=2)
    
    # Calculate and display duration
    end_time = time.time()
    duration = end_time - start_time
    hours, rem = divmod(duration, 3600)
    minutes, seconds = divmod(rem, 60)
    
    print(f"\n\nSuccessfully dumped {processed} documents to {output_file}")
    print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"End time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
    print(f"Duration: {int(hours)}h {int(minutes)}m {seconds:.2f}s")

if __name__ == '__main__':
    dump_collection_to_json()
