# Pharmacy Bill Entry Application

A comprehensive pharmacy billing system interface built with Python Tkinter, designed to replicate a professional GST-compliant purchase bill entry system with a fullscreen, color-coded interface matching the reference design.

## Project Structure

```
pharmacy-bill-entry
├── src
│   ├── main.py                # Entry point of the application
│   ├── ui                     # Contains UI components
│   │   ├── __init__.py        # Initializer for the ui package
│   │   └── bill_entry_window.py # UI layout for Purchase Bill Entry
│   ├── models                 # Contains data models
│   │   ├── __init__.py        # Initializer for the models package
│   │   ├── product.py         # Product class definition
│   │   └── bill.py            # Bill class definition
│   ├── controllers            # Contains application logic
│   │   ├── __init__.py        # Initializer for the controllers package
│   │   └── bill_controller.py  # Logic for handling user interactions
│   ├── utils                  # Utility functions
│   │   ├── __init__.py        # Initializer for the utils package
│   │   └── validators.py       # Input validation functions
│   └── data                   # Data handling
│       ├── __init__.py        # Initializer for the data package
│       └── database.py         # Functions for data storage
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Setup Instructions

1. **Clone the repository**:

   ```
   git clone <repository-url>
   cd pharmacy-bill-entry
   ```

2. **Install dependencies**:
   Ensure you have Python installed, then run:

   ```
   pip install -r requirements.txt
   ```

3. **Run the application**:
   Execute the main script:
   ```
   python src/main.py
   ```

## Usage Guidelines

- The application allows users to enter purchase bill details, including party information and product items.
- Users can add multiple items to a bill, save the bill, clear the form, or exit the application using the provided buttons in the UI.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
