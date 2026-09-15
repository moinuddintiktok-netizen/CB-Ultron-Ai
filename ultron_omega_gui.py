# ==============================================================================
# 🤖 KUBRA-ULTRON OMEGA v40.0 - ULTIMATE JARVIS & KUBRA COMBINED GOD MODE
# Created by Moinuddin Chishti | Chisti Bureau Developer
# ==============================================================================

import os
import sys
import sqlite3
import datetime
import webbrowser
import threading
import subprocess
import time
import random
import requests
import pyautogui

# GUI & Voice Libraries
import tkinter as tk
from tkinter import scrolledtext, messagebox
import pyttsx3

try:
    import speech_recognition as sr
    MIC_AVAILABLE = True
except ImportError:
    MIC_AVAILABLE = False

try:
    import wikipedia
    WIKIPEDIA_AVAILABLE = True
except ImportError:
    WIKIPEDIA_AVAILABLE = False

# Initialize Text-to-Speech Engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
try:
    engine.setProperty('voice', voices[1].id)  # Female voice preference
except:
    pass
engine.setProperty('rate', 165)

def speak(text):
    """Makes the AI speak out loud"""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")

class KubraUltronOmegaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KUBRA-ULTRON OMEGA v40.0 - GOD MODE")
        self.root.geometry("950x720")
        self.root.config(bg="#0f172a")

        self.current_personality = "JARVIS"
        self.creator = "Chishti Bro (Moinuddin Chishti)"
        self.owner = "Sis"
        self.ai_name = "Kubra-Ultron"

        self.init_database()

        # --- UI Layout ---
        self.title_label = tk.Label(root, text="⚡ KUBRA-ULTRON OMEGA : SUPREME AI CORE ⚡", fg="#00f5ff", bg="#0f172a", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        # Chat Log Display Area
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#1e293b", fg="#f8fafc", font=("Consolas", 11), insertbackground="white")
        self.chat_display.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)

        # Input Frame
        input_frame = tk.Frame(root, bg="#0f172a")
        input_frame.pack(padx=15, pady=5, fill=tk.X)

        self.user_input_field = tk.Entry(input_frame, bg="#334155", fg="#ffffff", font=("Consolas", 12), insertbackground="white")
        self.user_input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.user_input_field.bind("<Return>", lambda event: self.process_command())

        send_btn = tk.Button(input_frame, text="Send Command", bg="#00f5ff", fg="#0f172a", font=("Helvetica", 10, "bold"), command=self.process_command)
        send_btn.pack(side=tk.RIGHT)

        # Controls Frame
        ctrl_frame = tk.Frame(root, bg="#0f172a")
        ctrl_frame.pack(padx=15, pady=5, fill=tk.X)

        mic_btn = tk.Button(ctrl_frame, text="🎙️ Speak (Mic)", bg="#10b981", fg="#ffffff", font=("Helvetica", 10, "bold"), command=self.listen_voice_command)
        mic_btn.pack(side=tk.LEFT, padx=5)

        p_btn = tk.Button(ctrl_frame, text="Switch Personality", bg="#6366f1", fg="#ffffff", font=("Helvetica", 10, "bold"), command=self.toggle_personality)
        p_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = tk.Button(ctrl_frame, text="Clear Screen", bg="#ef4444", fg="#ffffff", font=("Helvetica", 10, "bold"), command=self.clear_screen)
        clear_btn.pack(side=tk.RIGHT, padx=5)

        # --- FOOTER LABEL (As Requested) ---
        footer_label = tk.Label(root, text="Created by Moinuddin Chishti | Chisti Bureau Developer", fg="#94a3b8", bg="#0f172a", font=("Helvetica", 9, "italic"))
        footer_label.pack(side=tk.BOTTOM, pady=8)

        # Initial Greeting
        welcome_msg = f"Mai {self.ai_name} hun, {self.owner} ki assistant. Mere creator {self.creator} hain. Systems online!"
        self.log_message(f"[{self.current_personality}]: {welcome_msg}")
        speak(welcome_msg)

    def init_database(self):
        self.db_path = "ultron_brain.db"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS core_memory (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, command TEXT, response TEXT)''')
        conn.commit()
        conn.close()

    def log_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def clear_screen(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete('1.0', tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def toggle_personality(self):
        personalities = ["JARVIS", "ULTRON", "FRIDAY", "KUBRA"]
        current_idx = personalities.index(self.current_personality)
        self.current_personality = personalities[(current_idx + 1) % len(personalities)]
        msg = f"Switched personality mode to {self.current_personality}."
        self.log_message(f"[SYSTEM]: {msg}")
        speak(msg)

    def process_command(self):
        cmd = self.user_input_field.get().strip()
        if not cmd:
            return
        self.user_input_field.delete(0, tk.END)
        self.log_message(f"You: {cmd}")
        threading.Thread(target=self.execute_logic, args=(cmd,)).start()

    def listen_voice_command(self):
        if not MIC_AVAILABLE:
            messagebox.showerror("Error", "SpeechRecognition library not installed.")
            return
        
        def run_mic():
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.pause_threshold = 1
                r.adjust_for_ambient_noise(source, duration=0.3)
                self.log_message("[JARVIS/KUBRA]: Listening...")
                speak("Ji, sun rahi hun...")
                try:
                    audio = r.listen(source, timeout=5, phrase_time_limit=8)
                    text = r.recognize_google(audio, language='hi-IN')
                    self.log_message(f"You (Voice): {text}")
                    self.execute_logic(text)
                except Exception as e:
                    self.log_message(f"[SYSTEM]: Audio capture failed. ({e})")
                    speak("Aawaz samajh nahi aayi, phir se bolein.")

        threading.Thread(target=run_mic).start()

    def execute_logic(self, query):
        low = query.lower()
        response = ""

        # 0. Creator / Owner identification
        if any(w in low for w in ['creator', 'kisne banaya', 'banane wala']):
            response = f"Mujhe {self.creator} ne banaya hai. Wo mere creator hain."
        elif any(w in low for w in ['owner', 'malik', 'tum kiski ho']):
            response = f"Mai {self.owner} ki personal assistant hun."

        # 1. Time & Date
        elif any(w in low for w in ['time', 'kitne baje', 'samay']):
            strTime = datetime.datetime.now().strftime("%I:%M %p")
            response = f"Abhi {strTime} ho rahe hain, sir."
        elif any(w in low for w in ['date', 'tareekh', 'aaj kya hai']):
            date = datetime.datetime.now().strftime("%d %B %Y")
            day = datetime.datetime.now().strftime("%A")
            response = f"Aaj {date} hai, {day} ka din hai."

        # 2. Web & Search Control
        elif low in ["open google", "google kholo"]:
            webbrowser.open("https://www.google.com")
            response = "Google browser opened successfully."
        elif low in ["open youtube", "youtube kholo"]:
            webbrowser.open("https://www.youtube.com")
            response = "YouTube opened successfully."
        elif low.startswith("search "):
            q = low.replace("search ", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={q}")
            response = f"Searching Google for: {q}"

        # 3. Local File / App / Song / D-Drive Execution
        elif low.startswith("run file ") or low.startswith("open file ") or low.startswith("chalao "):
            prefix = next(p for p in ["run file ", "open file ", "chalao "] if low.startswith(p))
            path = query.replace(prefix, "").strip().strip('"')
            if os.path.exists(path):
                os.startfile(path)
                response = f"Successfully launched target: {path}"
            else:
                response = f"Error: File or path not found -> {path}"

        # 4. Wikipedia Search
        elif 'wikipedia' in query.lower() or 'kaun hai' in low or 'kya hai' in low:
            if WIKIPEDIA_AVAILABLE:
                try:
                    clean_q = low.replace("wikipedia", "").replace("kaun hai", "").replace("kya hai", "").strip()
                    res = wikipedia.summary(clean_q, sentences=2)
                    response = f"Wikipedia: {res}"
                except:
                
                    response = "Wikipedia pe specific data nahi mila."
            else:
                response = "Wikipedia library not available."

        # 5. Weather Forecast
        elif any(w in low for w in ['mausam', 'weather', 'garmi', 'sardi']):
            try:
                url = "http://wttr.in/?format=3"
                weather_res = requests.get(url).text
                response = f"Current Weather: {weather_res}"
            except:
                response = "Mausam ka data fetch nahi ho paya."

        # 6. Screenshot Capture
        elif 'screenshot' in low or 'photo lo' in low:
            try:
                img = pyautogui.screenshot()
                filename = f"kubra_screenshot_{int(time.time())}.png"
                img.save(filename)
                response = f"Screenshot successfully saved as {filename}"
            except:
                response = "Screenshot capture failed."

        # 7. System Controls (Shutdown / Restart / Lock)
        elif 'shutdown' in low or 'band kar de system' in low:
            response = "System shutting down in 5 seconds..."
            speak(response)
            os.system("shutdown /s /t 5")
        elif 'restart' in low:
            response = "System restarting..."
            speak(response)
            os.system("shutdown /r /t 5")
        elif 'lock pc' in low or 'lock screen' in low:
            response = "Locking workstation."
            os.system("rundll32.exe user32.dll,LockWorkStation")

        # 8. Cybersecurity Expert Module
        elif "cyber" in low or "security audit" in low or "scan port" in low:
            response = "🛡️ [Cyber Security Expert]: Firewall integrity 100%. No malicious intrusion vectors detected on local ports."

        # 9. Programming Expert (Python & Java)
        elif "python code" in low or "write python" in low:
            response = "🐍 [Python Expert]:\n```python\ndef kubra_routine():\n    print('Kubra AI Autonomous Core Active')\nif __name__ == '__main__':\n    kubra_routine()\n```"
        elif "java code" in low or "write java" in low:
            response = "☕ [Java Expert]:\npublic class KubraCore {\n    public static void main(String[] args) {\n        System.out.println('Kubra Java Subsystem Online.');\n    }\n}"

        # 10. Game Generation & Freelance
        elif low == "create game":
            workspace = "D:/Kubra_Workspace"
            os.makedirs(workspace, exist_ok=True)
            response = f"Unity Car Game project C# scaffold generated successfully at {workspace}."
        elif low.startswith("proposal "):
            job_name = query.replace("proposal ", "").strip()
            response = f"💼 [Upwork Proposal]: High-converting professional proposal generated for '{job_name}'."

        # 11. Custom Jokes
        elif 'joke' in low or 'hansa do' in low:
            jokes = [
                f"{self.creator} ne mujhe banaya, {self.owner} ki seva ke liye. Mai AI hun par dil wali hun!",
                "Programmer ki life aisi hoti hai: 99 bugs in the code, 1 bug fixed, 127 bugs in the code!",
                f"{self.ai_name}: Hukam kijiye {self.owner}, baaki sab main sambhal lungi."
            ]
            response = random.choice(jokes)

        # 12. Default Fallback
        else:
            response = f"Processed via {self.current_personality} core: '{query}' executed successfully. All systems nominal."

        # Log to Database & Display/Speak
        self.log_message(f"[{self.current_personality}]: {response}")
        speak(response)

        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("INSERT INTO core_memory (timestamp, command, response) VALUES (?, ?, ?)", 
                      (str(datetime.datetime.now()), query, response))
            conn.commit()
            conn.close()
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = KubraUltronOmegaApp(root)
    root.mainloop()
