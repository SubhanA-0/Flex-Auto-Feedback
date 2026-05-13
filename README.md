FLEX Course Feedback Automator 🤖
Welcome! This script is designed to save you from the end-of-semester hassle by automating the repetitive course feedback process on the FAST-NUCES FLEX student portal.

Developed by Subhan Ahmed (BS AI, 24th Batch).

🚀 How to Use the Bot
Follow these simple steps to launch the automator and breeze through your evaluations:

1. Launch the Script
Open your terminal in the folder containing the project files and run the execution script:

Bash
./run.sh
OR 
Simply double click on the run.sh file present in the folder.

2. Wait for the Interface
Keep an eye on your terminal for background logs. Within a few seconds, the automator's User Interface (UI) window will pop up on your screen.

3. Enter Your Credentials
In the UI popup, enter your FLEX portal login details:

Roll Number: Enter this strictly in the standard university format (e.g., XXi-XXXX).

Password: Your standard FLEX password.

Select your preferred feedback rating from the dropdown menu, then click Launch Automation.

4. Browser Handoff
After clicking launch, wait a moment for an automated Google Chrome browser window to open. It will navigate to the FLEX login page and automatically type in the credentials you provided.

5. Manual Verification (Important!)
Because FLEX uses security measures to prevent bots, you need to assist it with the final login step:

Manually click the "I'm not a robot" reCAPTCHA box and solve the puzzle if it prompts you.

Manually click the "Sign In" button.

6. Let the Bot Take Over
Once you successfully log in and reach your dashboard, let go of the mouse! The bot will detect the URL change, automatically navigate to the Course Feedback section, and begin opening and submitting all your pending forms. Wait patiently while it works through the list.

7. Clean Up
Wait until the script finishes and gives you a success message. Once all the feedbacks have been submitted, you can exit the automator completely by closing the Chrome browser, the UI window, and your terminal.
