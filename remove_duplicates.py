import os
import pymongo
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGO_DB_NAME", "news")
    collection_name = os.getenv("MONGO_COLLECTION_NAME", "media")
    
    client = pymongo.MongoClient(mongo_uri)
    db = client[db_name]
    col = db[collection_name]
    
    print(f"Connecting to MongoDB: {mongo_uri}")
    print(f"Database: {db_name}, Collection: {collection_name}")
    print("Finding and removing duplicates... This may take a moment.")
    
    pipeline = [
        # Group by the unique key and collect all document _ids
        {
            "$group": {
                "_id": {
                    "datePub": "$datePub",
                    "headlines": "$headlines",
                    "src": "$src"
                },
                "all_ids": {"$push": "$_id"},
                "count": {"$sum": 1}
            }
        },
        # Keep only groups that have duplicates
        {
            "$match": {
                "count": {"$gt": 1}
            }
        }
    ]
    
    try:
        duplicates = list(col.aggregate(pipeline, allowDiskUse=True))
    except Exception as e:
        print(f"An error occurred during aggregation: {e}")
        return
        
    ids_to_delete = []
    stats = {}  # Tracks removal count by (year, source)
    
    for doc in duplicates:
        # Keep the first document, mark the rest for deletion
        dups_for_this_group = doc['all_ids'][1:]
        ids_to_delete.extend(dups_for_this_group)
        
        # Determine year and source for reporting
        date_pub = doc['_id'].get('datePub')
        src = doc['_id'].get('src')
        
        # Handle year extraction
        if date_pub and isinstance(date_pub, str):
            year = date_pub[:4]
        else:
            year = "Unknown"
            
        # Handle source
        if not src:
            src = "Unknown"
            
        key = (year, src)
        stats[key] = stats.get(key, 0) + len(dups_for_this_group)
        
    # Proceed to delete if there are duplicates
    if ids_to_delete:
        print(f"Executing deletion of {len(ids_to_delete)} records...")
        # Delete in chunks to avoid document size limits in case the list is very large
        chunk_size = 10000
        for i in range(0, len(ids_to_delete), chunk_size):
            chunk = ids_to_delete[i:i + chunk_size]
            col.delete_many({"_id": {"$in": chunk}})
    else:
        print("No duplicates found to remove.")
        return

    # Display the result
    print(f"\n{'Year':<10} | {'Source':<30} | {'Removed'}")
    print("-" * 65)
    
    total_removed = 0
    # Sort the stats by year then src
    for (year, src) in sorted(stats.keys()):
        count = stats[(year, src)]
        total_removed += count
        print(f"{str(year):<10} | {str(src):<30} | {count}")
        
    print("-" * 65)
    print(f"Total Records Removed: {total_removed}\n")

if __name__ == "__main__":
    main()
