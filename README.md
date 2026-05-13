# FLEX Course Feedback Automator 🤖
 
Automates the end-of-semester course evaluation process on the **FAST-NUCES FLEX** student portal.
 
> Developed by **Subhan Ahmed** — 24th Batch
 
---
 
## How to Use
 
### 1. Run the script
 
Open a terminal in the project folder and execute:
 
```bash
./run.sh
```
 
Or simply **double-click** `run.sh` in your file manager.
 
---
 
### 2. Wait for the UI window
 
A popup window will appear within a few seconds. Background logs will stream in the terminal — this is normal.
 
---
 
### 3. Enter your credentials
 
Fill in your FLEX portal details in the UI:
 
| Field | Details |
|-------|---------|
| **Roll Number** | Standard university format, e.g. `XXi-XXXX` |
| **Password** | Your regular FLEX password |
| **Feedback Rating** | Select from the dropdown menu |
 
Then click **Launch Automation**.
 
---
 
### 4. Chrome opens automatically
 
A Chrome window will launch and navigate to the FLEX login page, filling in your credentials automatically.
 
---
 
### 5. ⚠️ Manual step — complete the CAPTCHA
 
FLEX uses reCAPTCHA to block bots. You need to manually:
 
1. Click the **"I'm not a robot"** checkbox and solve the puzzle if prompted
2. Click the **"Sign In"** button
> **Note:** This is the only step requiring your input. Everything after login is fully automated.
 
---
 
### 6. Let the bot take over
 
Once you reach the dashboard, **step away from the mouse.**
 
The bot will:
- Detect the URL change after login
- Automatically navigate to the Course Feedback section
- Open and submit all pending feedback forms
Wait patiently while it works through the list.
 
---
 
### 7. Clean up
 
Once you see the success message and all feedback forms are submitted:
 
1. Close the Chrome browser window
2. Close the UI popup
3. Close the terminal
 
