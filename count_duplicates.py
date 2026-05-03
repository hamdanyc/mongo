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
    print("Counting duplicates... This may take a moment.")
    
    pipeline = [
        # Step 1: Group by the unique key (datePub, headlines, src) to find duplicates
        {
            "$group": {
                "_id": {
                    "datePub": "$datePub",
                    "headlines": "$headlines",
                    "src": "$src"
                },
                "count": {"$sum": 1}
            }
        },
        # Step 2: Keep only records that appear more than once
        {
            "$match": {
                "count": {"$gt": 1}
            }
        },
        # Step 3: Extract the year from datePub and handle missing src
        {
            "$addFields": {
                "year": {
                    "$cond": {
                        "if": {"$and": [{"$ne": ["$_id.datePub", None]}, {"$ne": ["$_id.datePub", ""]}]},
                        "then": {"$substrBytes": [{"$toString": "$_id.datePub"}, 0, 4]},
                        "else": "Unknown"
                    }
                },
                "src": {"$ifNull": ["$_id.src", "Unknown"]},
                # A duplicate count is (occurrences - 1)
                "duplicate_count": {"$subtract": ["$count", 1]}
            }
        },
        # Step 4: Group by year and src to get the total duplicate counts
        {
            "$group": {
                "_id": {
                    "year": "$year",
                    "src": "$src"
                },
                "total_duplicates": {"$sum": "$duplicate_count"}
            }
        },
        # Step 5: Sort by year and src for better readability
        {
            "$sort": {
                "_id.year": 1,
                "_id.src": 1
            }
        }
    ]
    
    try:
        results = list(col.aggregate(pipeline))
    except Exception as e:
        print(f"An error occurred during aggregation: {e}")
        return
    
    # Display the result
    print(f"\n{'Year':<10} | {'Source':<30} | {'Total Duplicates'}")
    print("-" * 65)
    
    total_duplicates = 0
    for doc in results:
        year = doc['_id']['year']
        src = doc['_id']['src']
        count = doc['total_duplicates']
        total_duplicates += count
        
        print(f"{str(year):<10} | {str(src):<30} | {count}")
        
    print("-" * 65)
    print(f"Total Duplicates Overall: {total_duplicates}\n")

if __name__ == "__main__":
    main()
