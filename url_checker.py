import curses
import requests
from concurrent.futures import ThreadPoolExecutor
from openpyxl import Workbook
import os

# ASCII Art for Title
TITLE_ASCII = """
##   ##  ######    ##                ######   ######   ####     ######   ######  ######   
##   ##  ##   ##   ##                # ## #   ##      ##  ##    # ## #   ##      ##   ##  
##   ##  ##   ##   ##                  ##     ##      ##          ##     ##      ##   ##  
##   ##  ##  ###   ##                  ##     #####    #####      ##     #####   ##  ###  
##   ##  #####     ##                  ##     ##           ##     ##     ##      #####    
##   ##  ## ###    ##   #              ##     ##      ##   ##     ##     ##      ## ###   
 #####   ##  ###   ######              ##     ######   #####      ##     ######  ##  ###  
"""

# Function to check URL validity
def check_url(url):
    try:
        response = requests.get(url.strip(), timeout=5)
        return url, response.status_code == 200  # URL is valid if status code is 200
    except requests.RequestException:
        return url, False  # Any exception means the URL is invalid

# Function to load URLs from urls.txt
def load_urls():
    try:
        with open("urls.txt", "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def save_to_excel(results, stdscr):
    height, width = stdscr.getmaxyx()
    
    # Clear bottom lines
    stdscr.move(height-3, 0)
    stdscr.clrtoeol()
    stdscr.move(height-2, 0)
    stdscr.clrtoeol()
    stdscr.move(height-1, 0)
    stdscr.clrtoeol()
    
    # Show prompt
    stdscr.addstr(height-2, 0, "Enter filename (without .xlsx): ", curses.color_pair(4))
    stdscr.refresh()
    
    # Initialize filename string
    filename = ""
    curses.echo()
    curses.curs_set(1)
    
    while True:
        ch = stdscr.getch()
        if ch == ord('\n'):
            break
        elif ch == 27:  # ESC key
            filename = "url_results"  # Default name
            break
        elif ch in (curses.KEY_BACKSPACE, 127):  # Handle backspace
            if filename:
                filename = filename[:-1]
                stdscr.move(height-2, len("Enter filename (without .xlsx): ") + len(filename))
                stdscr.addch(' ')
                stdscr.move(height-2, len("Enter filename (without .xlsx): ") + len(filename))
        elif ch in range(32, 127):  # Printable characters
            filename += chr(ch)
    
    # Reset terminal settings
    curses.noecho()
    curses.curs_set(0)
    
    # Use default name if empty
    if not filename:
        filename = "url_results"
    
    wb = Workbook()
    ws = wb.active
    ws.append(["URL", "Status"])
    
    for url, is_valid in results:
        status = "Valid" if is_valid else "Invalid"
        ws.append([url.strip(), status])
    
    file_path = os.path.join(os.getcwd(), f"{filename}.xlsx")
    wb.save(file_path)
    return file_path# Function to handle UI with curses
def url_checker(stdscr, urls):
    if not urls:
        return
        
    # Clear the screen completely at startup
    stdscr.clear()
    stdscr.refresh()
    
    height, width = stdscr.getmaxyx()
    
    if height < 25 or width < 100:
        stdscr.addstr(0, 0, "Terminal too small. Please resize to at least 100x25")
        stdscr.refresh()
        stdscr.getch()
        return

    # Reset all variables to initial state
    scroll_position = 0
    results = []
    
    # Clear any existing Excel results file
    if os.path.exists("url_results.xlsx"):
        os.remove("url_results.xlsx")

    curses.curs_set(0)

    try:
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        # Split ASCII art into lines and display each line separately
        ascii_lines = TITLE_ASCII.split('\n')
        for i, line in enumerate(ascii_lines):
            try:
                stdscr.addstr(i, 0, line[:width], curses.color_pair(3) | curses.A_BOLD)
            except curses.error:
                pass

        stdscr.addstr(8, 0, "Menu:", curses.color_pair(4) | curses.A_BOLD)
        stdscr.addstr(9, 0, "    ▶ Press 's' to Start Test", curses.color_pair(4))
        stdscr.addstr(10, 0, "    ▶ Press 'q' to Quit (saves results)", curses.color_pair(4))
        stdscr.addstr(11, 0, "    ▶ Press 'r' to Reload and Recheck URLs", curses.color_pair(4))
        
        stdscr.addstr(13, 0, "Navigation:", curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(14, 0, "    ↑ or ↓ - Scroll through results", curses.color_pair(3))
        stdscr.addstr(15, 0, "    ◼ - Status Display", curses.color_pair(3))
        stdscr.addstr(16, 0, "-"*60, curses.color_pair(3))
    except curses.error:
        pass
    while True:
        try:
            # Display results status
            stdscr.move(17, 0)
            stdscr.clrtobot()

            # Fetch URL statuses concurrently
            with ThreadPoolExecutor() as executor:
                results = list(executor.map(check_url, urls))

            # Count and display valid/invalid URLs
            valid_count = sum(1 for _, is_valid in results if is_valid)
            invalid_count = len(results) - valid_count
            stdscr.addstr(17, 0, f"Valid Count: {valid_count:<4}   Invalid Count: {invalid_count:<4}", curses.color_pair(3))

            # Display URL statuses
            height, width = stdscr.getmaxyx()
            max_display = height - 19
            visible_results = results[scroll_position:scroll_position + max_display]
            
            for i, (url, is_valid) in enumerate(visible_results):
                if i + 18 >= height - 1:
                    break
                status_text = "✔️ Valid" if is_valid else "❌ Invalid"
                color = curses.color_pair(1) if is_valid else curses.color_pair(2)
                display_url = url.strip()[:width-20]
                stdscr.addstr(i + 18, 0, f"{display_url:<{width-20}} Status: {status_text}", color)

            stdscr.refresh()

            # Handle keyboard input
            key = stdscr.getch()
            if key == ord('q'):
                file_path = save_to_excel(results, stdscr)
                stdscr.addstr(height - 1, 0, f"Results saved to {file_path}", curses.color_pair(3))
                stdscr.refresh()
                stdscr.getch()
                return  # Exit the function cleanly
            elif key == ord('r'):
                urls = load_urls()
                if not urls:
                    return
                scroll_position = 0
                stdscr.clear()  # Clear screen for reload
                continue
            elif key == curses.KEY_UP and scroll_position > 0:
                scroll_position -= 1
            elif key == curses.KEY_DOWN and scroll_position < len(results) - max_display:
                scroll_position += 1

        except curses.error:
            continue

# Load URLs from file
urls = load_urls()

# Run the curses application
curses.wrapper(url_checker, urls)