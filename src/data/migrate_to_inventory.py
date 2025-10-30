"""
Migrate data from bills_database.json to inventory.json
This is a one-time migration script
"""
import json
import os
from datetime import datetime

# Get the data directory
data_dir = os.path.dirname(os.path.abspath(__file__))
bills_file = os.path.join(data_dir, "bills_database.json")
inventory_file = os.path.join(data_dir, "inventory.json")

def migrate():
    """Migrate bills to inventory format"""
    if not os.path.exists(bills_file):
        print("❌ No bills_database.json found")
        return
    
    # Load bills
    with open(bills_file, 'r') as f:
        bills = json.load(f)
    
    print(f"📊 Found {len(bills)} bills to migrate")
    
    # Create inventory from bills
    inventory = []
    
    for bill in bills:
        if 'items' in bill:
            for item in bill['items']:
                # Add timestamps
                item['added_at'] = datetime.now().isoformat()
                item['last_updated'] = datetime.now().isoformat()
                inventory.append(item)
    
    # Save inventory
    with open(inventory_file, 'w') as f:
        json.dump(inventory, f, indent=2)
    
    print(f"✅ Migrated {len(inventory)} items to inventory.json")
    print(f"📁 Inventory saved to: {inventory_file}")

if __name__ == "__main__":
    migrate()
