from tkinter import Tk
from ui.bill_entry_window import BillEntryWindow

def main():
    root = Tk()
    root.title("Lic To: V.B. PHARMACY - 2025 - 2026    GST Ver: G2259PC - [Purchase Bill]")
    
    # Maximize window (not fullscreen) so Windows taskbar is visible
    root.state('zoomed')
    root.configure(bg="#E8D4E8")
    
    app = BillEntryWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()