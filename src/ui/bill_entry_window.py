from tkinter import Frame, Label, Button, Menu, Entry, Listbox, StringVar, END, Checkbutton, IntVar, messagebox
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.session_manager import SessionManager

class BillEntryWindow:
    def __init__(self, master):
        self.master = master
        
        # Initialize session manager with correct data directory path
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        self.session_manager = SessionManager(data_dir=data_dir)
        
        # Don't remove default title bar - keep it for taskbar visibility
        # master.overrideredirect(True)  # REMOVED - this was hiding app from taskbar
        
        # Sample data for party names (for testing autocomplete)
        self.parties = [
            "MEDIPILLAR DISTRIBUTORS",
            "MEDICO PHARMA SOLUTIONS",
            "MEDILIFE HEALTHCARE",
            "Apollo Distributors", 
            "Apollo Pharmacy Chain",
            "MedPlus Stores", 
            "MedPlus Wholesale",
            "Cipla Ltd", 
            "Cipla Healthcare",
            "Sun Pharma Distributors", 
            "Sun Healthcare Ltd",
            "Reddy's Lab",
            "Reddy's Pharmaceuticals",
            "Abbott India",
            "Pfizer Healthcare",
            "GSK Pharmaceuticals",
            "Mankind Pharma",
            "Lupin Limited",
            "Torrent Pharmaceuticals",
            "Cadila Healthcare"
        ]
        
        # Load inventory from database (replaces static medicine list)
        self.medicines = self.session_manager.get_inventory_items()
        
        # If no inventory exists, use some default items for initial testing
        if not self.medicines:
            print("⚠️ No inventory found in database. Add items and save to build inventory.")
            self.medicines = {
                "PARACETAMOL 500MG": {
                    'item_name': "PARACETAMOL 500MG",
                    'unit': "10",
                    'batch': '',
                    'exp_dt': '',
                    'mrp': '',
                    'ptr': '',
                    'gst_percent': '12'
                }
            }
        
        print(f"📦 Inventory loaded: {len(self.medicines)} unique items")
        
        # Inventory to store added items (current bill)
        self.inventory = []  # List of dictionaries with item details
        
        # Variables to track window state
        self.is_maximized = True
        
        # Create UI
        self.create_widgets()
        
        # Load previous session if exists
        self.load_previous_session()
        
        print("✅ Pharmacy Mock UI running successfully!")
    
    def create_widgets(self):
        # Main container
        main_container = Frame(self.master, bg="#E8D4E8")
        main_container.pack(fill="both", expand=True)
        
        # Menu bar (no custom title bar needed - using system title bar)
        self.create_menu_bar(main_container)
        
        # Navigation bar
        self.create_navigation_bar(main_container)
        
        # Main content area with purple/pink background
        content_frame = Frame(main_container, bg="#E8D4E8")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Purchase Bill Section
        self.create_purchase_bill_section(content_frame)
        
        print("UI implementation in progress...")
    
    def create_menu_bar(self, parent):
        """Create menu bar with all options"""
        menu_bar_frame = Frame(parent, bg="#F0F0F0", relief="raised", bd=1)
        menu_bar_frame.pack(fill="x", side="top")
        
        # Menu items
        menu_items = [
            "Supervisor", "Master", "Transaction", "MIS Reports", 
            "Financial Reports", "Other Facilities", "Window", "Exit"
        ]
        
        for item in menu_items:
            menu_btn = Button(menu_bar_frame, text=item, bg="#F0F0F0", fg="black",
                            font=("Arial", 9), relief="flat", padx=10, pady=3,
                            activebackground="#E0E0E0", cursor="hand2",
                            command=lambda m=item: self.menu_click(m))
            menu_btn.pack(side="left")
            
            # Add hover effect
            menu_btn.bind('<Enter>', lambda e, b=menu_btn: b.config(bg="#E0E0E0"))
            menu_btn.bind('<Leave>', lambda e, b=menu_btn: b.config(bg="#F0F0F0"))
    
    def create_navigation_bar(self, parent):
        """Create navigation bar with buttons"""
        nav_bar_frame = Frame(parent, bg="#4A90E2", relief="raised", bd=2, height=50)
        nav_bar_frame.pack(fill="x", side="top")
        nav_bar_frame.pack_propagate(False)
        
        # Navigation buttons
        nav_buttons = [
            ("GST", "#FF6B6B"),
            ("Item Master", "#4ECDC4"),
            ("Account Master", "#45B7D1"),
            ("Purchase Bill", "#FFA07A"),
            ("Sales Bill", "#98D8C8"),
            ("Sales Receipt", "#F7DC6F"),
            ("Purchase Payment", "#BB8FCE"),
            ("Cash Entry", "#85C1E2"),
            ("Bank Entry", "#F8B739"),
            ("Expiry List", "#52B788"),
            ("Today Status", "#FF8FA3"),
            ("GST Menu", "#A8DADC"),
            ("GST 2.0", "#E76F51")
        ]
        
        # Create buttons container - single row
        buttons_container = Frame(nav_bar_frame, bg="#4A90E2")
        buttons_container.pack(expand=True, fill="both", padx=5, pady=5)
        
        for idx, (button_text, color) in enumerate(nav_buttons):
            nav_btn = Button(buttons_container, text=button_text, 
                           bg=color, fg="white",
                           font=("Arial", 8, "bold"), 
                           relief="raised", bd=1, 
                           padx=3, pady=3,
                           width=8,
                           activebackground=color, 
                           cursor="hand2",
                           command=lambda bt=button_text: self.nav_click(bt))
            
            # Arrange all buttons in a single row
            nav_btn.pack(side="left", padx=2, pady=2)
    
    def create_purchase_bill_section(self, parent):
        """Create the Purchase Bill entry section"""
        # Get screen dimensions to calculate section size
        screen_width = self.master.winfo_screenwidth()
        section_width = int(screen_width * 0.66)  # 2/3 of screen width
        
        # Purchase Bill Frame - aligned left
        bill_frame = Frame(parent, bg="#E0D0E8", relief="groove", bd=2)
        bill_frame.pack(anchor="w", fill="x", padx=10, pady=10)
        
        # Row 1: EntNo and Party
        row1_frame = Frame(bill_frame, bg="#E0D0E8")
        row1_frame.pack(fill="x", padx=10, pady=8, anchor="w")
        
        # EntNo Label
        entno_label = Label(row1_frame, text="EntNo:", bg="#E0D0E8", fg="black",
                           font=("Arial", 10, "bold"), width=8, anchor="w")
        entno_label.pack(side="left", padx=(0, 5))
        
        # EntNo Input (auto-uppercase)
        self.entno_var = StringVar()
        self.entno_entry = Entry(row1_frame, textvariable=self.entno_var, width=15, font=("Arial", 10))
        self.entno_var.set("G")
        self.entno_var.trace('w', lambda *args: self.to_uppercase(self.entno_var))
        self.entno_entry.pack(side="left", padx=(0, 30))
        
        # Party Label
        party_label = Label(row1_frame, text="Party:", bg="#E0D0E8", fg="black",
                           font=("Arial", 10, "bold"), width=8, anchor="w")
        party_label.pack(side="left", padx=(0, 5))
        
        # Party Search Input with autocomplete (auto-uppercase)
        self.party_search_var = StringVar()
        self.party_search_var.trace('w', self.on_party_search)
        
        self.party_search_entry = Entry(row1_frame, textvariable=self.party_search_var,
                                        width=50, font=("Arial", 10))
        self.party_search_entry.pack(side="left", padx=(0, 5))
        
        # Create a frame for the dropdown (initially hidden) - below row1
        self.dropdown_frame = Frame(bill_frame, bg="white", relief="solid", bd=1)
        
        # Listbox for autocomplete suggestions
        self.party_listbox = Listbox(self.dropdown_frame, height=6, 
                                     font=("Arial", 9), bg="white",
                                     selectbackground="#0078D7", selectforeground="white")
        self.party_listbox.pack(fill="both", expand=True)
        
        # Bind selection event - only on click, not keyboard navigation
        self.party_listbox.bind('<Button-1>', self.on_party_click)
        self.party_listbox.bind('<Return>', self.on_listbox_enter)
        self.party_listbox.bind('<Escape>', self.on_listbox_escape)
        self.party_search_entry.bind('<Down>', self.on_down_arrow)
        self.party_search_entry.bind('<Up>', self.on_up_arrow)
        self.party_search_entry.bind('<Return>', self.on_enter_key)
        self.party_search_entry.bind('<Escape>', self.on_escape_key)
        
        # Variable to track if dropdown is shown
        self.dropdown_visible = False
        
        # Row 2: EntryDt, Credit/Debit dropdown, and two empty inputs
        row2_frame = Frame(bill_frame, bg="#E0D0E8")
        row2_frame.pack(fill="x", padx=10, pady=8, anchor="w")
        
        # EntryDt Label
        entrydt_label = Label(row2_frame, text="EntryDt:", bg="#E0D0E8", fg="black",
                             font=("Arial", 10, "bold"), width=8, anchor="w")
        entrydt_label.pack(side="left", padx=(0, 5))
        
        # EntryDt Input with today's date (pre-formatted with slashes)
        from datetime import datetime
        self.entrydt_entry = Entry(row2_frame, width=15, font=("Arial", 10))
        self.entrydt_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entrydt_entry.bind('<KeyRelease>', lambda e: self.smart_date_format(self.entrydt_entry))
        self.entrydt_entry.bind('<Return>', self.on_entrydt_enter)
        self.entrydt_entry.bind('<FocusIn>', self.on_entrydt_focus)
        self.entrydt_entry.bind('<Button-1>', self.on_entrydt_click)
        self.entrydt_entry.pack(side="left", padx=(0, 30))
        
        # Credit/Debit Dropdown
        from tkinter import ttk
        self.credit_debit_var = StringVar()
        self.credit_debit_var.set("Credit")
        self.credit_debit_dropdown = ttk.Combobox(row2_frame, textvariable=self.credit_debit_var,
                                             values=["Credit", "Debit"], state="readonly",
                                             width=12, font=("Arial", 10))
        self.credit_debit_dropdown.pack(side="left", padx=(0, 20))
        self.credit_debit_dropdown.bind('<Return>', self.on_credit_debit_enter)
        
        # Empty Input Box 1
        self.empty_input1_var = StringVar()
        self.empty_input1 = Entry(row2_frame, textvariable=self.empty_input1_var,
                                  width=20, font=("Arial", 10))
        self.empty_input1_var.trace('w', lambda *args: self.to_uppercase(self.empty_input1_var))
        self.empty_input1.pack(side="left", padx=(0, 20))
        self.empty_input1.bind('<Return>', self.on_empty_input1_enter)
        
        # Empty Input Box 2
        self.empty_input2_var = StringVar()
        self.empty_input2 = Entry(row2_frame, textvariable=self.empty_input2_var,
                                  width=20, font=("Arial", 10))
        self.empty_input2_var.trace('w', lambda *args: self.to_uppercase(self.empty_input2_var))
        self.empty_input2.pack(side="left", padx=(0, 5))
        
        # Row 3: BillNo, Tax dropdown, State dropdown, SCH DISC dropdown
        row3_frame = Frame(bill_frame, bg="#E0D0E8")
        row3_frame.pack(fill="x", padx=10, pady=8, anchor="w")
        
        # BillNo Label
        billno_label = Label(row3_frame, text="BillNo:", bg="#E0D0E8", fg="black",
                            font=("Arial", 10, "bold"), width=8, anchor="w")
        billno_label.pack(side="left", padx=(0, 5))
        
        # BillNo Input (auto-uppercase)
        self.billno_var = StringVar()
        self.billno_entry = Entry(row3_frame, textvariable=self.billno_var,
                                  width=15, font=("Arial", 10))
        self.billno_var.trace('w', lambda *args: self.to_uppercase(self.billno_var))
        self.billno_entry.pack(side="left", padx=(0, 30))
        self.billno_entry.bind('<Return>', self.on_billno_enter)
        self.billno_entry.bind('<FocusIn>', self.on_billno_focus)
        self.billno_entry.bind('<Button-1>', self.on_billno_click)
        
        # Tax Dropdown
        self.tax_var = StringVar()
        self.tax_var.set("Tax")
        tax_dropdown = ttk.Combobox(row3_frame, textvariable=self.tax_var,
                                   values=["Tax", "No Tax"], state="readonly",
                                   width=12, font=("Arial", 10))
        tax_dropdown.pack(side="left", padx=(0, 20))
        
        # State Dropdown (within state / outside state)
        self.state_var = StringVar()
        self.state_var.set("Within State")
        self.state_dropdown = ttk.Combobox(row3_frame, textvariable=self.state_var,
                                     values=["Within State", "Outside State"], state="readonly",
                                     width=15, font=("Arial", 10))
        self.state_dropdown.pack(side="left", padx=(0, 20))
        self.state_dropdown.bind('<Return>', self.on_state_enter)
        
        # SCH DISC Dropdown
        self.sch_disc_var = StringVar()
        self.sch_disc_var.set("SCH DISC")
        self.sch_disc_dropdown = ttk.Combobox(row3_frame, textvariable=self.sch_disc_var,
                                        values=["SCH DISC", "ABC DEG"], state="readonly",
                                        width=12, font=("Arial", 10))
        self.sch_disc_dropdown.pack(side="left", padx=(0, 5))
        self.sch_disc_dropdown.bind('<Return>', self.on_sch_disc_enter)
        
        # Row 4: Bill Dt, Empty input, Order button, Order checkbox, GST on Free checkbox, Tax Inclusive checkbox
        row4_frame = Frame(bill_frame, bg="#E0D0E8")
        row4_frame.pack(fill="x", padx=10, pady=8, anchor="w")
        
        # Bill Dt Label
        billdt_label = Label(row4_frame, text="Bill Dt:", bg="#E0D0E8", fg="black",
                            font=("Arial", 10, "bold"), width=8, anchor="w")
        billdt_label.pack(side="left", padx=(0, 5))
        
        # Bill Dt Input with today's date (same as EntryDt)
        self.billdt_entry = Entry(row4_frame, width=15, font=("Arial", 10))
        self.billdt_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.billdt_entry.bind('<KeyRelease>', lambda e: self.smart_date_format(self.billdt_entry))
        self.billdt_entry.bind('<Return>', self.on_billdt_enter)
        self.billdt_entry.bind('<FocusIn>', self.on_billdt_focus)
        self.billdt_entry.bind('<Button-1>', self.on_billdt_click)
        self.billdt_entry.pack(side="left", padx=(0, 30))
        
        # Empty Input Box
        self.row4_empty_var = StringVar()
        self.row4_empty_entry = Entry(row4_frame, textvariable=self.row4_empty_var,
                                      width=20, font=("Arial", 10))
        self.row4_empty_var.trace('w', lambda *args: self.to_uppercase(self.row4_empty_var))
        self.row4_empty_entry.pack(side="left", padx=(0, 20))
        self.row4_empty_entry.bind('<Return>', self.on_row4_empty_enter)
        
        # Order Button (no function)
        order_button = Button(row4_frame, text="Order", bg="#D0D0D0", fg="black",
                             font=("Arial", 9, "bold"), width=8, relief="raised")
        order_button.pack(side="left", padx=(0, 20))
        
        # Order Checkbox
        self.order_checkbox_var = IntVar()
        self.order_checkbox = Checkbutton(row4_frame, text="Order", variable=self.order_checkbox_var,
                                     bg="#E0D0E8", font=("Arial", 10))
        self.order_checkbox.pack(side="left", padx=(0, 15))
        self.order_checkbox.bind('<Return>', self.on_order_checkbox_enter)
        
        # GST on Free Checkbox
        self.gst_on_free_var = IntVar()
        self.gst_on_free_checkbox = Checkbutton(row4_frame, text="GST on Free", variable=self.gst_on_free_var,
                                           bg="#E0D0E8", font=("Arial", 10))
        self.gst_on_free_checkbox.pack(side="left", padx=(0, 15))
        self.gst_on_free_checkbox.bind('<Return>', self.on_gst_on_free_enter)
        
        # Tax Inclusive Checkbox
        self.tax_inclusive_var = IntVar()
        tax_inclusive_checkbox = Checkbutton(row4_frame, text="Tax Inclusive", variable=self.tax_inclusive_var,
                                            bg="#E0D0E8", font=("Arial", 10))
        tax_inclusive_checkbox.pack(side="left", padx=(0, 5))
        
        # Row 5: New MRP
        row5_frame = Frame(bill_frame, bg="#E0D0E8")
        row5_frame.pack(fill="x", padx=10, pady=8, anchor="w")
        
        # New MRP Label
        new_mrp_label = Label(row5_frame, text="New MRP:", bg="#E0D0E8", fg="black",
                             font=("Arial", 10, "bold"), width=8, anchor="w")
        new_mrp_label.pack(side="left", padx=(0, 5))
        
        # New MRP Input
        self.new_mrp_var = StringVar()
        self.new_mrp_entry = Entry(row5_frame, textvariable=self.new_mrp_var,
                                   width=15, font=("Arial", 10))
        self.new_mrp_entry.pack(side="left", padx=(0, 5))
        self.new_mrp_entry.bind('<Return>', self.on_new_mrp_enter)
        
        # Add Item Entry Table
        self.create_item_table(bill_frame)
        
        print("Purchase Bill section created - Rows 1-5 complete with Item Table")
    
    def format_date(self, *args):
        """Auto-format date as dd/mm/yyyy - only accept digits and auto-insert slashes"""
        current_value = self.entrydt_var.get()
        # Remove any non-digit characters except slashes
        digits_only = ''.join(c for c in current_value if c.isdigit())
        
        # Format with slashes
        formatted = ''
        if len(digits_only) > 0:
            formatted = digits_only[:2]
        if len(digits_only) > 2:
            formatted += '/' + digits_only[2:4]
        if len(digits_only) > 4:
            formatted += '/' + digits_only[4:8]
        
        # Only update if changed to avoid infinite loop
        if formatted != current_value:
            # Store cursor position
            widget = self.entrydt_entry
            try:
                cursor_pos = widget.index('insert')
                self.entrydt_var.set(formatted)
                # Adjust cursor position after formatting
                new_pos = min(cursor_pos, len(formatted))
                widget.icursor(new_pos)
            except:
                self.entrydt_var.set(formatted)
    
    def smart_date_format(self, entry_widget):
        """Format date with slashes always visible: dd/mm/yyyy"""
        current_value = entry_widget.get()
        
        # Remove all slashes and non-digits
        digits_only = ''.join(c for c in current_value if c.isdigit())
        
        # Limit to 8 digits (ddmmyyyy)
        digits_only = digits_only[:8]
        
        # Build formatted date with template "dd/mm/yyyy"
        template = "dd/mm/yyyy"
        result = list(template)
        
        # Fill in digits at appropriate positions (skip slash positions)
        digit_positions = [0, 1, 3, 4, 6, 7, 8, 9]  # Positions in "dd/mm/yyyy" where digits go
        for i, digit in enumerate(digits_only):
            if i < len(digit_positions):
                result[digit_positions[i]] = digit
        
        formatted = ''.join(result)
        
        # Get cursor position before update
        try:
            cursor_pos = entry_widget.index('insert')
        except:
            cursor_pos = 0
        
        # Update value
        entry_widget.delete(0, END)
        entry_widget.insert(0, formatted)
        
        # Restore cursor position, skip over slashes if needed
        if cursor_pos in [2, 5]:  # Slash positions
            cursor_pos += 1
        entry_widget.icursor(min(cursor_pos, len(formatted)))
    
    def expiry_date_format(self, entry_widget):
        """Format expiry date as mm/yy - e.g., 1525 becomes 15/25"""
        current_value = entry_widget.get()
        
        # Remove all slashes and non-digits
        digits_only = ''.join(c for c in current_value if c.isdigit())
        
        # Limit to 4 digits (mmyy)
        digits_only = digits_only[:4]
        
        # Build formatted date
        if len(digits_only) == 0:
            formatted = "mm/yy"
        elif len(digits_only) == 1:
            formatted = digits_only[0] + "m/yy"
        elif len(digits_only) == 2:
            formatted = digits_only[0:2] + "/yy"
        elif len(digits_only) == 3:
            formatted = digits_only[0:2] + "/" + digits_only[2] + "y"
        else:  # 4 or more digits
            formatted = digits_only[0:2] + "/" + digits_only[2:4]
        
        # Get cursor position before update
        try:
            cursor_pos = entry_widget.index('insert')
        except:
            cursor_pos = 0
        
        # Update value
        entry_widget.delete(0, END)
        entry_widget.insert(0, formatted)
        
        # Restore cursor position, skip over slash if needed
        if cursor_pos == 2:  # Slash position
            cursor_pos += 1
        entry_widget.icursor(min(cursor_pos, len(formatted)))
    
    def to_uppercase(self, string_var):
        """Convert input to uppercase automatically"""
        current_value = string_var.get()
        upper_value = current_value.upper()
        if current_value != upper_value:
            # Store cursor position
            widget = self.master.focus_get()
            if widget and hasattr(widget, 'index'):
                try:
                    cursor_pos = widget.index('insert')
                    string_var.set(upper_value)
                    widget.icursor(cursor_pos)
                except:
                    string_var.set(upper_value)
            else:
                string_var.set(upper_value)
    
    def on_party_search(self, *args):
        """Handle party search input and show matching results"""
        # First convert to uppercase
        self.to_uppercase(self.party_search_var)
        search_text = self.party_search_var.get()
        
        if not search_text:
            self.hide_dropdown()
            return
        
        # Filter parties that start with the search text (exact match from start)
        matches = [party for party in self.parties if party.startswith(search_text)]
        
        if matches:
            self.show_dropdown(matches)
        else:
            self.hide_dropdown()
    
    def show_dropdown(self, matches):
        """Show the dropdown with matching parties"""
        # Clear existing items
        self.party_listbox.delete(0, END)
        
        # Add matching items
        for match in matches:
            self.party_listbox.insert(END, match)
        
        if not self.dropdown_visible:
            # Position dropdown below party search entry
            self.dropdown_frame.pack(fill="x", padx=10, pady=(0, 5))
            self.dropdown_visible = True
    
    def hide_dropdown(self):
        """Hide the dropdown"""
        if self.dropdown_visible:
            self.dropdown_frame.pack_forget()
            self.dropdown_visible = False
    
    def on_party_click(self, event):
        """Handle mouse click selection from dropdown"""
        # Small delay to ensure selection is registered
        self.master.after(10, self.select_party_from_dropdown)
    
    def select_party_from_dropdown(self):
        """Select party from dropdown and move focus"""
        if self.party_listbox.curselection():
            selected_index = self.party_listbox.curselection()[0]
            selected_party = self.party_listbox.get(selected_index)
            self.party_search_var.set(selected_party)
            self.hide_dropdown()
            print(f"Party selected: {selected_party}")
            # Move focus to first empty input in row 2
            self.empty_input1.focus_set()
    
    def on_listbox_enter(self, event):
        """Handle Enter key when focused on listbox"""
        self.select_party_from_dropdown()
        return "break"  # Prevent default behavior
    
    def on_listbox_escape(self, event):
        """Handle Escape key in listbox - return to search box"""
        self.party_search_entry.focus_set()
        return "break"
    
    def on_down_arrow(self, event):
        """Handle down arrow key to move to dropdown"""
        if self.dropdown_visible and self.party_listbox.size() > 0:
            self.party_listbox.focus_set()
            self.party_listbox.selection_clear(0, END)
            self.party_listbox.selection_set(0)
            self.party_listbox.activate(0)
            return "break"  # Prevent default behavior
    
    def on_up_arrow(self, event):
        """Handle up arrow key in search box"""
        # If dropdown is visible, move to last item
        if self.dropdown_visible and self.party_listbox.size() > 0:
            self.party_listbox.focus_set()
            last_index = self.party_listbox.size() - 1
            self.party_listbox.selection_clear(0, END)
            self.party_listbox.selection_set(last_index)
            self.party_listbox.activate(last_index)
            self.party_listbox.see(last_index)
            return "break"
    
    def on_enter_key(self, event):
        """Handle Enter key in search box"""
        if self.dropdown_visible and self.party_listbox.size() > 0:
            # Select first item if dropdown is visible
            selected_party = self.party_listbox.get(0)
            self.party_search_var.set(selected_party)
            self.hide_dropdown()
            print(f"Party selected: {selected_party}")
            # Move focus to first empty input in row 2
            self.empty_input1.focus_set()
            return "break"
    
    def on_escape_key(self, event):
        """Handle Escape key in search box - hide dropdown"""
        if self.dropdown_visible:
            self.hide_dropdown()
            return "break"
    
    # ============ Item Search Methods (similar to Party search) ============
    
    def on_item_search(self, *args):
        """Handle item search input and show matching results"""
        # First convert to uppercase
        self.to_uppercase(self.item_search_var)
        search_text = self.item_search_var.get()
        
        if not search_text or len(search_text) < 2:
            self.hide_item_dropdown()
            return
        
        # Filter medicines that start with the search text (exact match from start)
        matches = [med_name for med_name in self.medicines.keys() if med_name.startswith(search_text)]
        
        if matches:
            self.show_item_dropdown(matches)
        else:
            self.hide_item_dropdown()
    
    def show_item_dropdown(self, matches):
        """Show the item dropdown with matching medicines"""
        # Clear existing items
        self.item_listbox.delete(0, END)
        
        # Add matching items
        for match in matches:
            self.item_listbox.insert(END, match)
        
        if not self.item_dropdown_visible:
            # Position dropdown below the search row (row 2 in table)
            self.item_dropdown_frame.grid(row=2, column=1, columnspan=15, sticky="ew", padx=0, pady=0)
            self.item_dropdown_visible = True
    
    def hide_item_dropdown(self):
        """Hide the item dropdown"""
        if self.item_dropdown_visible:
            self.item_dropdown_frame.grid_forget()
            self.item_dropdown_visible = False
    
    def on_item_click(self, event):
        """Handle mouse click selection from item dropdown"""
        # Small delay to ensure selection is registered
        self.master.after(10, self.select_item_from_dropdown)
    
    def select_item_from_dropdown(self):
        """Select item from dropdown and check for multiple batches"""
        if self.item_listbox.curselection():
            selected_index = self.item_listbox.curselection()[0]
            selected_item = self.item_listbox.get(selected_index)
            
            # Set the item name
            self.item_search_var.set(selected_item)
            
            # Get all batches for this item
            batches = self.session_manager.get_item_batches(selected_item)
            
            if len(batches) == 0:
                print(f"⚠️ No batch data found for {selected_item}")
                self.hide_item_dropdown()
            elif len(batches) == 1:
                # Single batch - auto-fill directly
                self.fill_item_fields(batches[0])
                self.hide_item_dropdown()
                # Move focus to Batch column
                if len(self.search_row_entries) > 2:
                    self.search_row_entries[2].focus_set()
            else:
                # Multiple batches - show batch selection dropdown
                self.hide_item_dropdown()
                self.show_batch_dropdown(batches)
    
    def on_item_listbox_enter(self, event):
        """Handle Enter key when focused on item listbox"""
        self.select_item_from_dropdown()
        return "break"
    
    def on_item_listbox_escape(self, event):
        """Handle Escape key in item listbox - return to item search box"""
        self.item_search_entry.focus_set()
        return "break"
    
    def on_item_down_arrow(self, event):
        """Handle down arrow key in item search to move to dropdown"""
        if self.item_dropdown_visible and self.item_listbox.size() > 0:
            self.item_listbox.focus_set()
            self.item_listbox.selection_clear(0, END)
            self.item_listbox.selection_set(0)
            self.item_listbox.activate(0)
            return "break"
    
    def on_item_up_arrow(self, event):
        """Handle up arrow key in item search box"""
        # If dropdown is visible, move to last item
        if self.item_dropdown_visible and self.item_listbox.size() > 0:
            self.item_listbox.focus_set()
            last_index = self.item_listbox.size() - 1
            self.item_listbox.selection_clear(0, END)
            self.item_listbox.selection_set(last_index)
            self.item_listbox.activate(last_index)
            self.item_listbox.see(last_index)
            return "break"
    
    def fill_item_fields(self, item_data):
        """Fill all item fields with the provided data"""
        if len(self.search_row_entries) > 11:
            # Unit (index 1)
            self.search_row_entries[1].delete(0, END)
            self.search_row_entries[1].insert(0, item_data.get('unit', ''))
            
            # Batch (index 2)
            self.search_row_entries[2].delete(0, END)
            self.search_row_entries[2].insert(0, item_data.get('batch', ''))
            
            # ExpDt (index 3)
            self.search_row_entries[3].delete(0, END)
            self.search_row_entries[3].insert(0, item_data.get('exp_dt', ''))
            
            # Mrp (index 4)
            self.search_row_entries[4].delete(0, END)
            self.search_row_entries[4].insert(0, item_data.get('mrp', ''))
            
            # PTR (index 7)
            self.search_row_entries[7].delete(0, END)
            self.search_row_entries[7].insert(0, item_data.get('ptr', ''))
            
            # Gst% (index 11)
            self.search_row_entries[11].delete(0, END)
            self.search_row_entries[11].insert(0, item_data.get('gst_percent', '0'))
            
            print(f"✅ Auto-filled: {item_data.get('item_name')} - Batch: {item_data.get('batch')}, Qty Avail: {item_data.get('qty')}, ExpDt: {item_data.get('exp_dt')}, Mrp: {item_data.get('mrp')}, PTR: {item_data.get('ptr')}")
    
    def show_batch_dropdown(self, batches):
        """Show dropdown with available batches for selection"""
        # Store batch data
        self.available_batches = batches
        
        # Create batch dropdown frame if it doesn't exist
        if not hasattr(self, 'batch_dropdown_frame'):
            self.batch_dropdown_frame = Frame(self.master, bg="white", relief="solid", bd=1)
            self.batch_listbox = Listbox(self.batch_dropdown_frame, 
                                        height=min(8, len(batches)),
                                        font=("Arial", 10),
                                        bg="white", fg="black",
                                        selectbackground="#1e3a8a",
                                        selectforeground="white",
                                        activestyle="none")
            self.batch_listbox.pack(fill="both", expand=True)
            
            # Bind events
            self.batch_listbox.bind('<Return>', self.on_batch_listbox_enter)
            self.batch_listbox.bind('<Escape>', self.on_batch_listbox_escape)
            self.batch_listbox.bind('<<ListboxSelect>>', lambda e: None)
            self.batch_listbox.bind('<Double-Button-1>', self.on_batch_click)
        
        # Clear and populate batch listbox
        self.batch_listbox.delete(0, END)
        for batch in batches:
            display_text = f"Batch: {batch['batch']} | Qty: {batch['qty']} | Exp: {batch['exp_dt']} | MRP: ₹{batch['mrp']} | PTR: ₹{batch['ptr']}"
            self.batch_listbox.insert(END, display_text)
        
        # Position the batch dropdown below the item search field
        search_entry_widget = self.search_row_entries[0]
        x = search_entry_widget.winfo_rootx() - self.master.winfo_rootx()
        y = search_entry_widget.winfo_rooty() - self.master.winfo_rooty() + search_entry_widget.winfo_height()
        width = 600  # Wider for batch details
        
        self.batch_dropdown_frame.place(x=x, y=y, width=width)
        self.batch_dropdown_visible = True
        
        # Focus on listbox and select first item
        self.batch_listbox.focus_set()
        self.batch_listbox.selection_set(0)
        self.batch_listbox.activate(0)
        
        print(f"📦 Showing {len(batches)} batches for selection")
    
    def hide_batch_dropdown(self):
        """Hide the batch selection dropdown"""
        if hasattr(self, 'batch_dropdown_frame'):
            self.batch_dropdown_frame.place_forget()
        self.batch_dropdown_visible = False
    
    def on_batch_click(self, event):
        """Handle mouse click selection from batch dropdown"""
        self.master.after(10, self.select_batch_from_dropdown)
    
    def select_batch_from_dropdown(self):
        """Select batch from dropdown and fill fields"""
        if self.batch_listbox.curselection():
            selected_index = self.batch_listbox.curselection()[0]
            selected_batch_data = self.available_batches[selected_index]
            
            # Fill all fields with selected batch data
            self.fill_item_fields(selected_batch_data)
            
            self.hide_batch_dropdown()
            
            # Move focus to Batch column (index 2) so user can edit/confirm
            if len(self.search_row_entries) > 2:
                self.search_row_entries[2].focus_set()
    
    def on_batch_listbox_enter(self, event):
        """Handle Enter key when focused on batch listbox"""
        self.select_batch_from_dropdown()
        return "break"
    
    def on_batch_listbox_escape(self, event):
        """Handle Escape key in batch listbox - return to item search box"""
        self.hide_batch_dropdown()
        self.item_search_entry.focus_set()
        return "break"
    
    def on_item_enter_key(self, event):
        """Handle Enter key in item search box"""
        if self.item_dropdown_visible and self.item_listbox.size() > 0:
            # Select first item if dropdown is visible
            selected_item = self.item_listbox.get(0)
            self.item_search_var.set(selected_item)
            
            # Get the unit for this medicine and set it in Unit field
            if selected_item in self.medicines:
                unit_value = self.medicines[selected_item]
                # Unit field is at index 1 in search_row_entries
                if len(self.search_row_entries) > 1:
                    unit_entry = self.search_row_entries[1]
                    unit_entry.delete(0, END)
                    unit_entry.insert(0, unit_value)
            
            self.hide_item_dropdown()
            print(f"Item selected: {selected_item}, Unit: {unit_value}")
            
            # Move focus to Batch column (index 2 in search_row_entries)
            if len(self.search_row_entries) > 2:
                self.search_row_entries[2].focus_set()
            return "break"
    
    def on_item_escape_key(self, event):
        """Handle Escape key in item search box - hide dropdown"""
        if self.item_dropdown_visible:
            self.hide_item_dropdown()
            return "break"
    
    # ============ End of Item Search Methods ============
    
    def on_empty_input1_enter(self, event):
        """Handle Enter key in empty input 1 - move to EntryDt and select all"""
        self.entrydt_entry.focus_set()
        self.schedule_select_all(self.entrydt_entry)
        return "break"
    
    def on_entrydt_focus(self, event):
        """Auto-select all text when EntryDt gets focus"""
        self.schedule_select_all(self.entrydt_entry)
    
    def on_entrydt_click(self, event):
        """Handle mouse click on EntryDt - select all text"""
        return self.handle_entry_click_select_all(self.entrydt_entry)
    
    def on_entrydt_enter(self, event):
        """Handle Enter key in EntryDt - move to BillNo"""
        self.billno_entry.focus_set()
        self.schedule_select_all(self.billno_entry)
        return "break"
    
    def on_billno_focus(self, event):
        """Auto-select all text when BillNo gets focus"""
        self.schedule_select_all(self.billno_entry)
    
    def on_billno_click(self, event):
        """Handle mouse click on BillNo - select all text"""
        return self.handle_entry_click_select_all(self.billno_entry)
    
    def on_billno_enter(self, event):
        """Handle Enter key in BillNo - move to Bill Dt and select all"""
        self.billdt_entry.focus_set()
        self.schedule_select_all(self.billdt_entry)
        return "break"
    
    def on_billdt_focus(self, event):
        """Auto-select all text when Bill Dt gets focus"""
        self.schedule_select_all(self.billdt_entry)
    
    def on_billdt_click(self, event):
        """Handle mouse click on Bill Dt - select all text"""
        return self.handle_entry_click_select_all(self.billdt_entry)

    def on_billdt_enter(self, event):
        """Handle Enter key in Bill Dt - move to Credit/Debit dropdown"""
        self.credit_debit_dropdown.focus_set()
        return "break"
    
    def on_credit_debit_enter(self, event):
        """Handle Enter key in Credit/Debit dropdown - move to State dropdown"""
        self.state_dropdown.focus_set()
        return "break"
    
    def on_state_enter(self, event):
        """Handle Enter key in State dropdown - move to SCH DISC dropdown"""
        self.sch_disc_dropdown.focus_set()
        return "break"
    
    def on_sch_disc_enter(self, event):
        """Handle Enter key in SCH DISC dropdown - move to Row 4 empty input"""
        self.row4_empty_entry.focus_set()
        return "break"
    
    def on_row4_empty_enter(self, event):
        """Handle Enter key in Row 4 empty input - move to Order checkbox"""
        self.order_checkbox.focus_set()
        return "break"
    
    def on_order_checkbox_enter(self, event):
        """Handle Enter key in Order checkbox - move to GST on Free checkbox"""
        self.gst_on_free_checkbox.focus_set()
        return "break"
    
    def on_gst_on_free_enter(self, event):
        """Handle Enter key in GST on Free checkbox - move to first table cell (Item Name)"""
        if hasattr(self, 'search_row_entries') and len(self.search_row_entries) > 0:
            # Focus on Item Name entry of search row (index 0 is Item Name)
            self.search_row_entries[0].focus_set()
        return "break"
    
    def on_mrp_enter(self, event):
        """Handle Enter key in Mrp field - move to New MRP"""
        if hasattr(self, 'new_mrp_entry'):
            self.new_mrp_entry.focus_set()
        return "break"
    
    def on_new_mrp_enter(self, event):
        """Handle Enter key in New MRP - move to Qty field in table"""
        # Focus on Qty field in search row (index 5: 0=Item, 1=Unit, 2=Batch, 3=ExpDt, 4=Mrp, 5=Qty)
        if hasattr(self, 'search_row_entries') and len(self.search_row_entries) > 5:
            # Focus on Qty entry of search row
            self.search_row_entries[5].focus_set()
        return "break"
    
    def on_locat_enter(self, event):
        """Handle Enter key in Locat field - save item and add to table"""
        # Collect all field values from search row
        # search_row_entries indices: 0=Item, 1=Unit, 2=Batch, 3=ExpDt, 4=Mrp, 5=Qty, 
        #                              6=Fr, 7=PTR, 8=D%, 9=Disc, 10=BASE, 11=Gst%, 
        #                              12=Amount, 13=L.P., 14=Locat
        
        if not hasattr(self, 'search_row_entries') or len(self.search_row_entries) < 15:
            return "break"
        
        # Get values from all fields
        item_data = {
            'item_name': self.search_row_entries[0].get().strip(),
            'unit': self.search_row_entries[1].get().strip(),
            'batch': self.search_row_entries[2].get().strip(),
            'exp_dt': self.search_row_entries[3].get().strip(),
            'mrp': self.search_row_entries[4].get().strip(),
            'qty': self.search_row_entries[5].get().strip(),
            'fr': self.search_row_entries[6].get().strip(),
            'ptr': self.search_row_entries[7].get().strip(),
            'd_percent': self.search_row_entries[8].get().strip(),
            'disc': self.search_row_entries[9].get().strip(),
            'base': self.search_row_entries[10].get().strip(),
            'gst_percent': self.search_row_entries[11].get().strip(),
            'amount': self.search_row_entries[12].get().strip(),
            'lp': self.search_row_entries[13].get().strip(),
            'locat': self.search_row_entries[14].get().strip()
        }
        
        # Validate that at least item name is entered
        if not item_data['item_name']:
            print("Error: Item name is required")
            return "break"
        
        # Add to inventory
        self.inventory.append(item_data)
        
        # Add row to table display
        self.add_item_row_to_table(item_data)
        
        # Auto-save session state
        self.save_current_session()
        
        # Clear search row for next entry
        self.clear_search_row()
        
        # Move focus back to Item Name for next entry
        self.search_row_entries[0].focus_set()
        
        print(f"Item added: {item_data['item_name']} - Total items: {len(self.inventory)}")
        return "break"
    
    def add_item_row_to_table(self, item_data):
        """Add a new data row to the table with serial number"""
        # Calculate row number (search row is at grid row 1, data rows start at row 2)
        # But we need to account for the item dropdown frame which might be at row 2
        row_num = len(self.item_data_rows) + 2  # Header=0, Search=1, Data starts at 2
        
        # Serial number
        serial_num = len(self.item_data_rows) + 1
        
        # Column headers for reference
        headers = ["No", "Item Name", "Unit", "Batch", "ExpDt", "Mrp", "Qty", "Fr", 
                   "PTR", "D%", "Disc", "BASE", "Gst%", "Amount", "L.P.", "Locat"]
        widths = [4, 25, 6, 12, 10, 10, 6, 4, 10, 6, 10, 10, 6, 12, 12, 8]
        
        # Data values in order
        values = [
            str(serial_num),
            item_data['item_name'],
            item_data['unit'],
            item_data['batch'],
            item_data['exp_dt'],
            item_data['mrp'],
            item_data['qty'],
            item_data['fr'],
            item_data['ptr'],
            item_data['d_percent'],
            item_data['disc'],
            item_data['base'],
            item_data['gst_percent'],
            item_data['amount'],
            item_data['lp'],
            item_data['locat']
        ]
        
        # Create row entries
        row_entries = []
        for col, (header, width, value) in enumerate(zip(headers, widths, values)):
            # Create label for display (non-editable for now)
            label = Label(self.table_frame, text=value, 
                         bg="white", font=("Arial", 9),
                         width=width, relief="solid", bd=1, anchor="w")
            label.grid(row=row_num, column=col, sticky="ew", padx=0, pady=0)
            row_entries.append(label)
        
        # Store row data
        self.item_data_rows.append({
            'data': item_data,
            'widgets': row_entries,
            'row_num': row_num
        })
        
        # Update scroll region
        self.table_frame.update_idletasks()
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))
    
    def clear_search_row(self):
        """Clear all fields in the search row"""
        for i, entry in enumerate(self.search_row_entries):
            entry.delete(0, END)
            # Reset default values for D%, Disc, BASE, Gst%
            if i in [8, 9, 10, 11]:  # D%, Disc, BASE, Gst%
                entry.insert(0, "0")
    
    def calculate_base(self):
        """Calculate BASE = Qty * PTR"""
        try:
            # Get Qty (index 5) and PTR (index 7)
            qty = self.search_row_entries[5].get().strip()
            ptr = self.search_row_entries[7].get().strip()
            
            if qty and ptr:
                qty_val = float(qty)
                ptr_val = float(ptr)
                base_val = qty_val * ptr_val
                
                # Set BASE (index 10)
                self.search_row_entries[10].delete(0, END)
                self.search_row_entries[10].insert(0, f"{base_val:.2f}")
                
                # Recalculate Amount as BASE changed
                self.calculate_amount()
        except ValueError:
            # Invalid number, ignore
            pass
    
    def calculate_amount(self):
        """Calculate Amount = BASE + (BASE * Gst% / 100)"""
        try:
            # Get BASE (index 10) and Gst% (index 11)
            base = self.search_row_entries[10].get().strip()
            gst_percent = self.search_row_entries[11].get().strip()
            
            if base and gst_percent:
                base_val = float(base)
                gst_val = float(gst_percent)
                
                # Amount = BASE + (BASE * Gst% / 100)
                amount_val = base_val + (base_val * gst_val / 100)
                
                # Set Amount (index 12)
                self.search_row_entries[12].delete(0, END)
                self.search_row_entries[12].insert(0, f"{amount_val:.2f}")
        except ValueError:
            # Invalid number, ignore
            pass
    
    def delete_all_items(self):
        """Delete all items from the table and clear inventory"""
        # Confirm deletion
        if len(self.inventory) == 0:
            print("No items to delete")
            return
        
        # Remove all data row widgets from table
        for row_data in self.item_data_rows:
            for widget in row_data['widgets']:
                widget.destroy()
        
        # Clear data structures
        self.item_data_rows.clear()
        self.inventory.clear()
        
        # Clear session state
        self.session_manager.clear_session()
        
        # Update scroll region
        self.table_frame.update_idletasks()
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))
        
        print("All items deleted and session cleared")
    
    def create_item_table(self, parent):
        """Create the item entry table with columns and two empty rows"""
        # Table frame with border
        table_container = Frame(parent, bg="#E0D0E8", relief="groove", bd=2)
        table_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header frame with title and delete button
        header_frame = Frame(table_container, bg="#E0D0E8")
        header_frame.pack(fill="x", pady=(5, 10))
        
        # Table title
        table_title = Label(header_frame, text="Item Details", bg="#E0D0E8", 
                           font=("Arial", 11, "bold"), fg="#333333")
        table_title.pack(side="left", padx=(10, 0))
        
        # Delete All button
        delete_all_btn = Button(header_frame, text="Delete All Items", 
                               bg="#FF4444", fg="white", font=("Arial", 9, "bold"),
                               command=self.delete_all_items, cursor="hand2",
                               relief="raised", bd=2, padx=10, pady=5)
        delete_all_btn.pack(side="right", padx=(0, 10))
        
        # Create canvas with scrollbar for table
        from tkinter import Canvas, Scrollbar, VERTICAL, HORIZONTAL
        
        canvas_frame = Frame(table_container, bg="white")
        canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Canvas for scrolling
        self.table_canvas = Canvas(canvas_frame, bg="white", highlightthickness=0)
        
        # Scrollbars
        v_scrollbar = Scrollbar(canvas_frame, orient=VERTICAL, command=self.table_canvas.yview)
        h_scrollbar = Scrollbar(canvas_frame, orient=HORIZONTAL, command=self.table_canvas.xview)
        
        # Configure canvas
        self.table_canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and canvas
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        self.table_canvas.pack(side="left", fill="both", expand=True)
        
        # Frame inside canvas for table content
        self.table_frame = Frame(self.table_canvas, bg="white")
        self.canvas_window = self.table_canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        
        # Table headers and column widths
        headers = ["No", "Item Name", "Unit", "Batch", "ExpDt", "Mrp", "Qty", "Fr", 
                   "PTR", "D%", "Disc", "BASE", "Gst%", "Amount", "L.P.", "Locat"]
        
        widths = [4, 25, 6, 12, 10, 10, 6, 4, 10, 6, 10, 10, 6, 12, 12, 8]
        
        # Header row with colored background
        header_frame = Frame(self.table_frame, bg="#4A90E2", relief="raised", bd=1)
        header_frame.grid(row=0, column=0, columnspan=len(headers), sticky="ew")
        
        for col, (header, width) in enumerate(zip(headers, widths)):
            header_label = Label(header_frame, text=header, bg="#4A90E2", fg="white",
                                font=("Arial", 9, "bold"), width=width, 
                                relief="raised", bd=1, anchor="center")
            header_label.grid(row=0, column=col, sticky="ew", padx=1, pady=1)
        
        # Store entry widgets for navigation
        self.item_entries = []
        self.item_data_rows = []  # Store actual data rows (with serial numbers)
        
        # Create first row - this is the SEARCH/INPUT row (no serial number)
        search_row_entries = []
        
        for col, (header, width) in enumerate(zip(headers, widths)):
            if col == 0:  # No column - leave empty for search row
                entry = Label(self.table_frame, text="", 
                             bg="#FFFACD", font=("Arial", 9),
                             width=width, relief="solid", bd=1, anchor="center")
            else:
                # Create editable entry
                entry_var = StringVar()
                entry = Entry(self.table_frame, textvariable=entry_var,
                             width=width, font=("Arial", 9), 
                             relief="solid", bd=1, justify="left",
                             bg="#FFFACD")  # Light yellow background for search row
                
                # Special handling for Item Name column (col 1)
                if col == 1:
                    # Store item name entry and variable
                    self.item_search_var = entry_var
                    self.item_search_entry = entry
                    
                    # Bind search functionality (like party search)
                    self.item_search_var.trace('w', self.on_item_search)
                    entry.bind('<Down>', self.on_item_down_arrow)
                    entry.bind('<Up>', self.on_item_up_arrow)
                    entry.bind('<Return>', self.on_item_enter_key)
                    entry.bind('<Escape>', self.on_item_escape_key)
                elif col == 3:  # Batch column - auto-select on focus
                    entry.bind('<FocusIn>', lambda e, ent=entry: self.schedule_select_all(ent))
                    entry.bind('<Button-1>', lambda e, ent=entry: self.handle_entry_click_select_all(ent))
                    entry.bind('<Return>', lambda e, c=col: self.on_search_row_enter(e, c))
                    entry.bind('<Tab>', lambda e, c=col: self.on_search_row_tab(e, c))
                elif col == 4:  # ExpDt column - auto-select on focus
                    entry.bind('<FocusIn>', lambda e, ent=entry: self.schedule_select_all(ent))
                    entry.bind('<Button-1>', lambda e, ent=entry: self.handle_entry_click_select_all(ent))
                    entry.bind('<Return>', lambda e, c=col: self.on_search_row_enter(e, c))
                    entry.bind('<Tab>', lambda e, c=col: self.on_search_row_tab(e, c))
                elif col == 5:  # Mrp column - auto-select on focus and special navigation to New MRP
                    entry.bind('<FocusIn>', lambda e, ent=entry: self.schedule_select_all(ent))
                    entry.bind('<Button-1>', lambda e, ent=entry: self.handle_entry_click_select_all(ent))
                    entry.bind('<Return>', self.on_mrp_enter)
                    entry.bind('<Tab>', lambda e, c=col: self.on_search_row_tab(e, c))
                elif col == 8:  # PTR column - auto-select on focus and calculate BASE on change
                    entry.bind('<FocusIn>', lambda e, ent=entry: self.schedule_select_all(ent))
                    entry.bind('<Button-1>', lambda e, ent=entry: self.handle_entry_click_select_all(ent))
                    entry.bind('<KeyRelease>', lambda e: self.calculate_base())
                    entry.bind('<Return>', lambda e, c=col: self.on_search_row_enter(e, c))
                    entry.bind('<Tab>', lambda e, c=col: self.on_search_row_tab(e, c))
                elif col == 9:  # D% column - auto-select on focus
                    entry.bind('<FocusIn>', lambda e, ent=entry: self.schedule_select_all(ent))
                    entry.bind('<Button-1>', lambda e, ent=entry: self.handle_entry_click_select_all(ent))
                    entry.bind('<Return>', lambda e, c=col: self.on_search_row_enter(e, c))
                    entry.bind('<Tab>', lambda e, c=col: self.on_search_row_tab(e, c))
                elif col == 10:  # Disc column - auto-select on focus
                    entry.bind('<FocusIn>', lambda e, ent=entry: self.schedule_select_all(ent))
                    entry.bind('<Button-1>', lambda e, ent=entry: self.handle_entry_click_select_all(ent))
                    entry.bind('<Return>', lambda e, c=col: self.on_search_row_enter(e, c))
                    entry.bind('<Tab>', lambda e, c=col: self.on_search_row_tab(e, c))
                elif col == 12:  # Gst% column - auto-select on focus and calculate Amount
                    entry.bind('<FocusIn>', lambda e, ent=entry: self.schedule_select_all(ent))
                    entry.bind('<Button-1>', lambda e, ent=entry: self.handle_entry_click_select_all(ent))
                    entry.bind('<KeyRelease>', lambda e: self.calculate_amount())
                    entry.bind('<Return>', lambda e, c=col: self.on_search_row_enter(e, c))
                    entry.bind('<Tab>', lambda e, c=col: self.on_search_row_tab(e, c))
                elif col == 15:  # Locat column - auto-select on focus and save item on Enter
                    entry.bind('<FocusIn>', lambda e, ent=entry: self.schedule_select_all(ent))
                    entry.bind('<Button-1>', lambda e, ent=entry: self.handle_entry_click_select_all(ent))
                    entry.bind('<Return>', self.on_locat_enter)
                    entry.bind('<Tab>', lambda e, c=col: self.on_search_row_tab(e, c))
                else:
                    # Bind Enter key for navigation in search row
                    entry.bind('<Return>', lambda e, c=col: self.on_search_row_enter(e, c))
                    
                    # Bind Tab key for navigation
                    entry.bind('<Tab>', lambda e, c=col: self.on_search_row_tab(e, c))
                
                # Calculate BASE when Qty changes (col 6)
                if col == 6:  # Qty column
                    entry.bind('<KeyRelease>', lambda e: self.calculate_base())
                
                # Auto-uppercase for text columns
                if col in [1, 3, 15]:  # Item Name, Batch, Locat
                    entry_var.trace('w', lambda *args, v=entry_var: self.to_uppercase(v))
                
                # Expiry date formatting for ExpDt column (mm/yy format)
                if col == 4:  # ExpDt
                    entry.bind('<KeyRelease>', lambda e, ent=entry: self.expiry_date_format(ent))
                
                # Set default value "0" for D%, Disc, BASE, Gst% columns
                if col in [9, 10, 11, 12]:  # D%, Disc, BASE, Gst%
                    entry_var.set("0")
                
                search_row_entries.append(entry)
            
            entry.grid(row=1, column=col, sticky="ew", padx=0, pady=0)
        
        # Store search row entries separately
        self.search_row_entries = search_row_entries
        
        # Create a frame for the item dropdown (initially hidden) - will be positioned below table
        self.item_dropdown_frame = Frame(self.table_frame, bg="white", relief="solid", bd=1)
        
        # Listbox for item autocomplete suggestions
        self.item_listbox = Listbox(self.item_dropdown_frame, height=6, 
                                     font=("Arial", 9), bg="white",
                                     selectbackground="#0078D7", selectforeground="white")
        self.item_listbox.pack(fill="both", expand=True)
        
        # Bind selection events for item listbox
        self.item_listbox.bind('<Button-1>', self.on_item_click)
        self.item_listbox.bind('<Return>', self.on_item_listbox_enter)
        self.item_listbox.bind('<Escape>', self.on_item_listbox_escape)
        
        # Variables to track if dropdowns are shown
        self.item_dropdown_visible = False
        self.batch_dropdown_visible = False
        
        # Configure grid weights for proper column sizing
        for col in range(len(headers)):
            self.table_frame.grid_columnconfigure(col, weight=0)
        
        # Update scroll region
        self.table_frame.update_idletasks()
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))
        
        # Bind canvas resize to adjust scroll region
        self.table_frame.bind('<Configure>', lambda e: self.table_canvas.configure(
            scrollregion=self.table_canvas.bbox("all")))
        
        # Footer with Save to Inventory button
        footer_frame = Frame(table_container, bg="#E0D0E8")
        footer_frame.pack(fill="x", pady=(10, 5))
        
        # Save to Inventory button (green)
        self.save_btn = Button(footer_frame, text="💾 Save to Inventory", 
                               bg="#28A745", fg="white", font=("Arial", 11, "bold"),
                               command=self.save_bill_to_database, cursor="hand2",
                               relief="raised", bd=3, padx=20, pady=10)
        self.save_btn.pack(side="right", padx=10)
        
        # Status label
        self.status_label = Label(footer_frame, text="", bg="#E0D0E8", 
                                  font=("Arial", 9), fg="#666666")
        self.status_label.pack(side="left", padx=10)
        
        print("Item table created with 16 columns and search row (light yellow)")
    
    def on_search_row_enter(self, event, col):
        """Handle Enter key in search row cells - move to next cell with special navigation"""
        # col is the index in headers array (1=Item Name, 2=Unit, etc.)
        # search_row_entries is 0-indexed (0=Item Name, 1=Unit, etc.)
        # Headers: ["No", "Item Name", "Unit", "Batch", "ExpDt", "Mrp", "Qty", "Fr", 
        #           "PTR", "D%", "Disc", "BASE", "Gst%", "Amount", "L.P.", "Locat"]
        search_row_index = col - 1  # Convert from header index to search_row_entries index
        
        # Special navigation rules:
        # From Disc (col 10, index 9) → skip BASE, go to Gst% (col 12, index 11)
        if col == 10:  # Disc column
            if len(self.search_row_entries) > 11:
                self.search_row_entries[11].focus_set()  # Go to Gst%
            return "break"
        
        # From Gst% (col 12, index 11) → skip Amount and L.P., go to Locat (col 15, index 14)
        if col == 12:  # Gst% column
            if len(self.search_row_entries) > 14:
                self.search_row_entries[14].focus_set()  # Go to Locat
            return "break"
        
        # Default: Move to next column in search row
        if search_row_index < len(self.search_row_entries) - 1:
            self.search_row_entries[search_row_index + 1].focus_set()
        else:
            # Last cell in search row - stay here for now (will add item later)
            print("Last cell in search row - ready to add item")
        return "break"
    
    def on_search_row_tab(self, event, col):
        """Handle Tab key in search row cells - move to next cell"""
        # Same as Enter for now
        return self.on_search_row_enter(event, col)
    
    def on_table_enter(self, event, row, col):
        """Handle Enter key in data row cells - move to next cell"""
        # Move to next column in same row
        if col < len(self.item_entries[row]) - 1:
            self.item_entries[row][col + 1].focus_set()
        else:
            # Move to first column of next row
            if row < len(self.item_entries) - 1:
                self.item_entries[row + 1][0].focus_set()
            else:
                # Last cell - could add new row or move to next section
                print("Last cell in table - end of item entry")
        return "break"
    
    def on_table_tab(self, event, row, col):
        """Handle Tab key in data row cells - move to next cell"""
        # Same as Enter for now
        return self.on_table_enter(event, row, col)
    
    def select_all_text(self, entry_widget):
        """Select all text in an entry widget if it still has focus"""
        try:
            if entry_widget and entry_widget == self.master.focus_get():
                entry_widget.selection_range(0, END)
                entry_widget.icursor(END)
        except Exception as e:
            print(f"Error selecting text: {e}")

    def schedule_select_all(self, entry_widget, delays=(0, 40, 120)):
        """Schedule select-all across small delays to survive widget updates"""
        for delay in delays:
            self.master.after(delay, lambda ew=entry_widget: self.select_all_text(ew))

    def handle_entry_click_select_all(self, entry_widget):
        """Common handler for mouse click bindings that should select all"""
        self.schedule_select_all(entry_widget)
        return "break"
    
    def nav_click(self, button_name):
        """Handle navigation button clicks"""
        print(f"Navigation button clicked: {button_name}")
        if button_name == "Purchase Bill":
            print("Opening Purchase Bill entry...")
    
    def menu_click(self, menu_name):
        """Handle menu clicks"""
        print(f"Menu clicked: {menu_name}")
        if menu_name == "Exit":
            self.master.quit()
    
    # ============ Session Management & Database Methods ============
    
    def save_current_session(self):
        """Auto-save current session state (temporary)"""
        try:
            session_data = {
                'inventory': self.inventory,
                'party': self.party_search_var.get() if hasattr(self, 'party_search_var') else '',
                'entry_dt': self.entrydt_entry.get() if hasattr(self, 'entrydt_entry') else '',
                'bill_no': self.billno_entry.get() if hasattr(self, 'billno_entry') else '',
                'bill_dt': self.billdt_entry.get() if hasattr(self, 'billdt_entry') else ''
            }
            self.session_manager.save_session(session_data)
            self.update_status("Session auto-saved")
        except Exception as e:
            print(f"Error saving session: {e}")
    
    def load_previous_session(self):
        """Load previous session if exists"""
        try:
            session_data = self.session_manager.load_session()
            if session_data and session_data.get('inventory'):
                # Restore inventory
                self.inventory = session_data['inventory']
                
                # Restore form fields if they exist
                if hasattr(self, 'party_search_var') and session_data.get('party'):
                    self.party_search_var.set(session_data['party'])
                if hasattr(self, 'entrydt_entry') and session_data.get('entry_dt'):
                    self.entrydt_entry.delete(0, END)
                    self.entrydt_entry.insert(0, session_data['entry_dt'])
                if hasattr(self, 'billno_entry') and session_data.get('bill_no'):
                    self.billno_entry.delete(0, END)
                    self.billno_entry.insert(0, session_data['bill_no'])
                if hasattr(self, 'billdt_entry') and session_data.get('bill_dt'):
                    self.billdt_entry.delete(0, END)
                    self.billdt_entry.insert(0, session_data['bill_dt'])
                
                # Restore table rows
                for item_data in self.inventory:
                    self.add_item_row_to_table(item_data)
                
                self.update_status(f"Session restored: {len(self.inventory)} items")
                print(f"✅ Previous session loaded: {len(self.inventory)} items")
        except Exception as e:
            print(f"Error loading session: {e}")
    
    def save_bill_to_database(self):
        """Save items to inventory (not bill - just inventory management)"""
        if len(self.inventory) == 0:
            messagebox.showwarning("No Items", "Please add items before saving to inventory.")
            return
        
        # Calculate totals for display
        total_amount = sum(float(item.get('amount', 0) or 0) for item in self.inventory)
        
        # Save items to inventory (batch-aware: updates qty if item+batch exists)
        if self.session_manager.save_to_inventory(self.inventory):
            # Refresh inventory search list
            self.medicines = self.session_manager.get_inventory_items()
            print(f"📦 Inventory refreshed: {len(self.medicines)} unique items")
            
            messagebox.showinfo("Success", 
                              f"Items saved to inventory successfully!\n\n"
                              f"Items: {len(self.inventory)}\n"
                              f"Total Amount: ₹{total_amount:.2f}")
            
            # Clear everything after successful save
            self.delete_all_items()
            self.update_status("Items saved to inventory ✅")
        else:
            messagebox.showerror("Error", "Failed to save items to inventory.")
    
    def update_status(self, message):
        """Update status label"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
            # Clear status after 3 seconds
            self.master.after(3000, lambda: self.status_label.config(text=""))

