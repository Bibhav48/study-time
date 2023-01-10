import tkinter as tk
from tkinter import ttk, simpledialog
import sqlite3
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

DB_NAME = 'study_sessions.db'
ENV_FILE = '.env'


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

    def init_db(self):
        with open('schema.sql', 'r') as f:
            self.cursor.executescript(f.read())
        self.conn.commit()

    def insert_session(self, date, start_time, end_time, study_time, other_time):
        self.cursor.execute('''
        INSERT INTO study_sessions (date, start_time, end_time, study_time, other_time)
        VALUES (?, ?, ?, ?, ?)
        ''', (date, start_time, end_time, study_time, other_time))
        self.conn.commit()

    def get_study_record(self):
        self.cursor.execute('''
        SELECT date, SUM(study_time) as total_study_time, SUM(other_time) as total_other_time, COUNT(*) as session_count
        FROM study_sessions
        GROUP BY date
        ORDER BY date DESC
        ''')
        return self.cursor.fetchall()

    def get_detailed_record(self, date):
        self.cursor.execute('''
        SELECT start_time, end_time, study_time, other_time
        FROM study_sessions
        WHERE date = ?
        ORDER BY start_time
        ''', (date,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


class Stopwatch:
    def __init__(self, master):
        self.master = master
        self.master.title("Study Timer")
        self.master.resizable(False, False)

        self.db = Database()

        self.time_sec = 0
        self.other_time = 0
        self.running = False
        self.paused = False
        self.start_time = None

        self.create_widgets()

    def create_widgets(self):
        self.time_label = ttk.Label(self.master, font=(
            "ds-digital bold", 100), foreground="cyan", background="black")
        self.time_label.pack(anchor='center')

        self.start_stop_button = ttk.Button(
            self.master, text="Start", command=self.start_stop)
        self.start_stop_button.pack(padx=10)

        self.pause_play_button = ttk.Button(
            self.master, text="Pause", command=self.pause_play, state=tk.DISABLED)
        self.pause_play_button.pack(padx=10)

        self.update_time()

    def start_stop(self):
        if not self.running:
            self.running = True
            self.start_time = datetime.now()
            self.start_stop_button.config(text="Stop")
            self.pause_play_button.config(state=tk.NORMAL)
        else:
            self.running = False
            end_time = datetime.now()

            self.db.insert_session(
                self.start_time.strftime("%Y-%m-%d"),
                self.start_time.strftime("%H:%M:%S"),
                end_time.strftime("%H:%M:%S"),
                self.time_sec,
                self.other_time
            )

            self.master.quit()

    def pause_play(self):
        if not self.paused:
            self.paused = True
            self.pause_play_button.config(text="Play")
        else:
            self.paused = False
            self.pause_play_button.config(text="Pause")

    def update_time(self):
        if self.running and not self.paused:
            self.time_sec += 1
        elif self.running and self.paused:
            self.other_time += 1

        hours, remainder = divmod(self.time_sec, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
        self.time_label.config(text=time_str)

        self.master.after(1000, self.update_time)


def print_overview(db):
    results = db.get_study_record()
    print("\nStudy Session Overview:")
    print("----------------------")
    for date, total_study_time, total_other_time, session_count in results:
        print(f"Date: {date}")
        print(f"Total Study Time: {timedelta(seconds=total_study_time)}")
        print(f"Total Other Time: {timedelta(seconds=total_other_time)}")
        print(f"Number of Sessions: {session_count}")
        print()


def print_detailed_record(db, date):
    results = db.get_detailed_record(date)
    print(f"\nDetailed Study Record for {date}:")
    print("----------------------------------")
    for start_time, end_time, study_time, other_time in results:
        print(f"Session: {start_time} - {end_time}")
        print(f"Study Time: {timedelta(seconds=study_time)}")
        print(f"Other Time: {timedelta(seconds=other_time)}")
        print()


def initialize_if_needed():
    if not os.path.exists(ENV_FILE) or not os.path.exists(DB_NAME):
        db = Database()
        db.init_db()
        with open(ENV_FILE, 'w') as f:
            f.write("DB_INITIALIZED=true\n")
        print("Database initialized successfully.")
    else:
        load_dotenv()
        if os.getenv('DB_INITIALIZED') != 'true':
            db = Database()
            db.init_db()
            with open(ENV_FILE, 'w') as f:
                f.write("DB_INITIALIZED=true\n")
            print("Database re-initialized successfully.")


def display_records_gui(db):
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    choice = simpledialog.askstring(
        "Record Display", "Choose display format:\n1. Overview\n2. Detailed Record\nEnter 1 or 2:")

    if choice == '1':
        print_overview(db)
    elif choice == '2':
        date = simpledialog.askstring(
            "Date Selection", "Enter date (YYYY-MM-DD):")
        if date:
            print_detailed_record(db, date)
    else:
        print("Invalid choice. Exiting.")


def display_records_cli(db):
    choice = input(
        "Choose display format:\n1. Overview\n2. Detailed Record\nEnter 1 or 2: ")

    if choice == '1':
        print_overview(db)
    elif choice == '2':
        date = input("Enter date (YYYY-MM-DD): ")
        print_detailed_record(db, date)
    else:
        print("Invalid choice. Exiting.")


def main():
    initialize_if_needed()

    root = tk.Tk()
    root.configure()
    app = Stopwatch(root)
    root.mainloop()
    app.db.close()

    db = Database()

    # Prompt for GUI or CLI
    interface_choice = input(
        "Choose interface for record display:\n1. GUI\n2. CLI\nEnter 1 or 2: ")

    if interface_choice == '1':
        display_records_gui(db)
    elif interface_choice == '2':
        display_records_cli(db)
    else:
        print("Invalid choice. Exiting.")

    db.close()


if __name__ == "__main__":
    main()
