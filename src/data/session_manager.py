"""
Session Manager for Pharmacy Bill Entry
Handles temporary session state and permanent database storage
"""
import json
import os
from datetime import datetime

class SessionManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.session_file = os.path.join(data_dir, "current_session.json")
        self.database_file = os.path.join(data_dir, "bills_database.json")  # Legacy - keeping for reference
        self.inventory_file = os.path.join(data_dir, "inventory.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
    
    def save_session(self, session_data):
        """Save current session state (temporary - auto-saves on changes)"""
        try:
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving session: {e}")
            return False
    
    def load_session(self):
        """Load last session state if exists"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error loading session: {e}")
            return None
    
    def clear_session(self):
        """Clear current session file"""
        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
            return True
        except Exception as e:
            print(f"Error clearing session: {e}")
            return False
    
    def save_to_inventory(self, items):
        """Save items to inventory. If item+batch exists, increase qty; otherwise add new entry"""
        try:
            # Load existing inventory
            inventory = []
            if os.path.exists(self.inventory_file):
                with open(self.inventory_file, 'r') as f:
                    inventory = json.load(f)
            
            items_added = 0
            items_updated = 0
            
            # Process each item
            for new_item in items:
                item_name = new_item.get('item_name', '').strip().upper()
                batch = new_item.get('batch', '').strip().upper()
                new_qty = float(new_item.get('qty', 0) or 0)
                
                if not item_name or not batch:
                    continue
                
                # Check if item+batch combination exists
                found = False
                for existing_item in inventory:
                    if (existing_item.get('item_name', '').strip().upper() == item_name and 
                        existing_item.get('batch', '').strip().upper() == batch):
                        # Update quantity
                        old_qty = float(existing_item.get('qty', 0) or 0)
                        existing_item['qty'] = str(old_qty + new_qty)
                        existing_item['last_updated'] = datetime.now().isoformat()
                        found = True
                        items_updated += 1
                        print(f"📦 Updated: {item_name} (Batch: {batch}) - Qty: {old_qty} → {old_qty + new_qty}")
                        break
                
                if not found:
                    # Add new entry
                    new_item['added_at'] = datetime.now().isoformat()
                    new_item['last_updated'] = datetime.now().isoformat()
                    inventory.append(new_item)
                    items_added += 1
                    print(f"✨ Added: {item_name} (Batch: {batch}) - Qty: {new_qty}")
            
            # Save inventory
            with open(self.inventory_file, 'w') as f:
                json.dump(inventory, f, indent=2)
            
            print(f"✅ Inventory saved: {items_added} new, {items_updated} updated")
            return True
        except Exception as e:
            print(f"❌ Error saving to inventory: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_all_bills(self):
        """Get all saved bills from database"""
        try:
            if os.path.exists(self.database_file):
                with open(self.database_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading database: {e}")
            return []
    
    def get_inventory_items(self):
        """Get all inventory items grouped by name for search"""
        try:
            if not os.path.exists(self.inventory_file):
                print(f"⚠️ No inventory file found at {self.inventory_file}")
                return {}
            
            with open(self.inventory_file, 'r') as f:
                inventory_list = json.load(f)
            
            print(f"📊 Found {len(inventory_list)} items in inventory")
            
            # Group by item name (for search dropdown)
            # For each item name, keep the latest batch details
            inventory_dict = {}
            
            for item in inventory_list:
                item_name = item.get('item_name', '').strip()
                if item_name:
                    # If item doesn't exist or this entry is newer, use it
                    if item_name not in inventory_dict:
                        inventory_dict[item_name] = {
                            'item_name': item_name,
                            'unit': item.get('unit', ''),
                            'batch': item.get('batch', ''),
                            'exp_dt': item.get('exp_dt', ''),
                            'mrp': item.get('mrp', ''),
                            'ptr': item.get('ptr', ''),
                            'gst_percent': item.get('gst_percent', '0')
                        }
            
            print(f"📦 Loaded {len(inventory_dict)} unique item names")
            return inventory_dict
        except Exception as e:
            print(f"❌ Error loading inventory: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def get_item_batches(self, item_name):
        """Get all available batches for a specific item"""
        try:
            if not os.path.exists(self.inventory_file):
                return []
            
            with open(self.inventory_file, 'r') as f:
                inventory_list = json.load(f)
            
            # Filter batches for this specific item
            batches = []
            for item in inventory_list:
                if item.get('item_name', '').strip().upper() == item_name.strip().upper():
                    batches.append({
                        'item_name': item.get('item_name', ''),
                        'unit': item.get('unit', ''),
                        'batch': item.get('batch', ''),
                        'exp_dt': item.get('exp_dt', ''),
                        'mrp': item.get('mrp', ''),
                        'qty': item.get('qty', '0'),
                        'ptr': item.get('ptr', ''),
                        'gst_percent': item.get('gst_percent', '0')
                    })
            
            return batches
        except Exception as e:
            print(f"❌ Error getting batches: {e}")
            return []
