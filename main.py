import time
import threading
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Global Control Flag ---
stop_flag = False

# --- Selenium Automation Logic ---
def setup_driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def run_automation(username, password, target_index):
    global stop_flag
    driver = None
    try:
        driver = setup_driver()
        print("Opening FLEX Login...")
        driver.get("https://flexstudent.nu.edu.pk/Login")
        
        # --- 1. LOGIN PHASE ---
        if stop_flag: return
        
        print("Filling credentials...")
        roll_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Roll Number')]"))
        )
        roll_input.send_keys(username)
        
        pass_input = driver.find_element(By.XPATH, "//input[@type='password']")
        pass_input.send_keys(password)
        
        print("*********************************************************")
        print("ACTION REQUIRED: Please solve the reCAPTCHA in the browser")
        print("and click the 'Sign In' button manually. Waiting...")
        print("*********************************************************")
        
        WebDriverWait(driver, 300).until(
            lambda d: "Login" not in d.current_url
        )
        
        print("Login success detected! Navigating to feedback...")
        time.sleep(3) 
        
        # --- 2. SIDEBAR NAVIGATION PHASE ---
        if stop_flag: return
        
        try:
            print("Looking for 'Course Feedback' in the sidebar menu...")
            menu_item = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Course Feedback')]"))
            )
            
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu_item)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", menu_item)
            print("Navigating to feedback page...")
            
        except Exception as e:
            raise Exception(f"Could not find the 'Course Feedback' button in the sidebar. Error: {e}")
            
        # --- 3. FEEDBACK LOOP PHASE ---
        while not stop_flag:
            print("\nWaiting dynamically for the courses table to load...")
            
            try:
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Give Feedback')]"))
                )
            except Exception:
                print("\n===========================================")
                print("SUCCESS: No more pending feedbacks found!")
                print("===========================================")
                # Notify the user via a popup that the job is completely done
                root.after(0, lambda: messagebox.showinfo("Success", "All feedbacks have been submitted successfully!"))
                break
            
            if stop_flag: break
                
            buttons = driver.find_elements(By.XPATH, "//*[contains(text(), 'Give Feedback')]")
            print(f"Found {len(buttons)} forms remaining. Opening the next one...")
            
            driver.execute_script("arguments[0].click();", buttons[0])
            
            # --- THE TIMING FIX IS HERE ---
            try:
                print("Waiting for form to render...")
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='radio']"))
                )
                # CRITICAL: Even if the first radio button appears, the rest of the form might still be loading.
                # Force a 2-second wait to let the entire DOM populate all 50+ questions.
                time.sleep(2) 
            except:
                raise Exception("The feedback form took too long to load or failed to display radio buttons.")
            
            if stop_flag: break 
            
            radios = driver.find_elements(By.XPATH, "//input[@type='radio']")
            print(f"Found {len(radios)} radio buttons. Filling options...")
            
            # Fill the radio buttons with small, safe delays
            for i in range(target_index, len(radios), 5):
                if stop_flag: break
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radios[i])
                time.sleep(0.1) # Brief pause after scrolling so the browser registers the position
                driver.execute_script("arguments[0].click();", radios[i])
                    
            if stop_flag: break 
            
            # Wait for and click the submit button securely
            print("Submitting form...")
            try:
                submit_btn = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'save')] | //input[@type='submit']"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
                time.sleep(0.5) # Crucial pause before submitting
                driver.execute_script("arguments[0].click();", submit_btn)
                print("Form submitted successfully! Waiting for redirection...")
            except Exception as e:
                raise Exception(f"Failed to find or click the Submit button. Error: {e}")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        # NO MORE SILENT CRASHES: Push the error to the Tkinter UI so you can read it!
        root.after(0, lambda err=str(e): messagebox.showerror("Automation Error", f"The bot crashed!\n\nReason:\n{err}"))
    finally:
        if stop_flag:
            print("\nAutomation stopped manually by user.")
        if driver:
            print("Closing browser...")
            driver.quit() 
        reset_ui() 

# --- GUI Setup ---
def show_gui():
    global root, submit_btn, stop_btn, roll_entry, pass_entry, rating_var
    
    root = tk.Tk()
    root.title("FLEX Automator")
    root.geometry("420x420")
    root.configure(bg="#ffffff")

    blue_primary = "#0052cc"
    red_stop = "#cc0000"
    font_main = ("Helvetica", 10)

    def launch_thread():
        global stop_flag
        roll = roll_entry.get().strip()
        password = pass_entry.get().strip()
        
        if not roll or not password:
            messagebox.showerror("Error", "Please enter both your Roll Number and Password.")
            return

        # --- THE FLIPPED SCALE FIX IS HERE ---
        rating_map = {
            "Option 1 (Leftmost - Usually Strongly Agree)": 0,
            "Option 2 (Agree)": 1,
            "Option 3 (Neutral)": 2,
            "Option 4 (Disagree)": 3,
            "Option 5 (Rightmost - Usually Strongly Disagree)": 4
        }
        target_index = rating_map.get(rating_var.get(), 0) # Defaults to Option 1 (Leftmost)
        
        stop_flag = False
        submit_btn.config(state="disabled", bg="#cccccc")
        stop_btn.config(state="normal", bg=red_stop)
        
        print("Launching Background Task...")
        threading.Thread(target=run_automation, args=(roll, password, target_index), daemon=True).start()

    def stop_thread():
        global stop_flag
        print("\nStop signal sent. Waiting for script to safely halt...")
        stop_flag = True
        stop_btn.config(state="disabled", text="Stopping...")

    tk.Label(root, text="FLEX Course Feedback Agent", font=("Helvetica", 14, "bold"), bg="#ffffff", fg=blue_primary).pack(pady=20)

    tk.Label(root, text="Roll Number:", font=font_main, bg="#ffffff").pack(anchor="w", padx=50)
    roll_entry = tk.Entry(root, font=font_main, width=35, bg="#f0f4f8", relief="solid", borderwidth=1)
    roll_entry.pack(pady=5)

    tk.Label(root, text="FLEX Password:", font=font_main, bg="#ffffff").pack(anchor="w", padx=50)
    pass_entry = tk.Entry(root, font=font_main, width=35, show="*", bg="#f0f4f8", relief="solid", borderwidth=1)
    pass_entry.pack(pady=5)

    tk.Label(root, text="Fill all forms with:", font=font_main, bg="#ffffff").pack(anchor="w", padx=50)
    rating_var = tk.StringVar(root)
    rating_var.set("Option 1 (Leftmost - Usually Strongly Agree)")
    
    # Updated dropdown options
    dropdown = tk.OptionMenu(root, rating_var, 
                             "Option 1 (Strongly Agree)", 
                             "Option 2 (Agree)", 
                             "Option 3 (Neutral)", 
                             "Option 4 (Disagree)", 
                             "Option 5 (Strongly Disagree)")
    dropdown.config(bg="#ffffff", font=font_main, width=33, relief="solid", borderwidth=1)
    dropdown.pack(pady=10)

    btn_frame = tk.Frame(root, bg="#ffffff")
    btn_frame.pack(pady=20)

    submit_btn = tk.Button(btn_frame, text="Launch Automation", font=("Helvetica", 10, "bold"), width=18, bg=blue_primary, fg="#ffffff", command=launch_thread, relief="flat")
    submit_btn.grid(row=0, column=0, padx=5)

    stop_btn = tk.Button(btn_frame, text="Stop", font=("Helvetica", 10, "bold"), width=10, bg="#cccccc", fg="#ffffff", command=stop_thread, relief="flat", state="disabled")
    stop_btn.grid(row=0, column=1, padx=5)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def reset_ui():
    try:
        root.after(0, lambda: submit_btn.config(state="normal", bg="#0052cc"))
        root.after(0, lambda: stop_btn.config(state="disabled", bg="#cccccc", text="Stop"))
    except:
        pass 

def on_closing():
    global stop_flag
    stop_flag = True
    root.destroy()

if __name__ == "__main__":
    show_gui()