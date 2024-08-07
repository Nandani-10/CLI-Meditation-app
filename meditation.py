import time
from datetime import datetime, timedelta
import json
import os

# Load or initialize user data
def load_data(filename='user_data.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    else:
        return {
            'progress': [],
            'mood_log': [],
            'streak': 0,
            'last_meditation_date': None
        }

# Save user data
def save_data(data, filename='user_data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Initialize user data
user_data = load_data()

# Main menu for the CLI Meditation App
def main_menu():
    while True:
        print("\nMeditation CLI App")
        print("1. Start a guided meditation session")
        print("2. Set a meditation timer")
        print("3. View progress")
        print("4. Log mood")
        print("5. Customize session")
        print("6. View statistics")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            guided_meditation()
        elif choice == '2':
            meditation_timer()
        elif choice == '3':
            view_progress()
        elif choice == '4':
            log_mood()
        elif choice == '5':
            customize_session()
        elif choice == '6':
            view_statistics()
        elif choice == '7':
            save_data(user_data)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Guided meditation session
def guided_meditation():
    print("\nGuided Meditation Session")
    
    prompts = [
        "Close your eyes and take a deep breath...",
        "Feel the sensation of the air entering your lungs...",
        "Slowly exhale and release any tension...",
        "Focus on your breathing. Inhale... Exhale...",
        "Notice the thoughts that come to your mind and let them pass...",
        "When you're ready, slowly open your eyes."
    ]

    for prompt in prompts:
        print(prompt)
        time.sleep(5)

    user_data['progress'].append({
        'type': 'guided',
        'date': datetime.now().isoformat()
    })

    update_streak()
    print("Meditation session complete.")

# Meditation timer session
def meditation_timer():
    try:
        minutes = int(input("Enter the number of minutes for your meditation: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return
    
    duration = minutes * 60
    end_time = datetime.now() + timedelta(seconds=duration)
    
    print(f"Meditation timer set for {minutes} minutes. Close your eyes and relax.")

    while duration > 0:
        remaining_time = end_time - datetime.now()
        minutes_left, seconds_left = divmod(int(remaining_time.total_seconds()), 60)
        timer_display = f"\rTime left: {minutes_left:02}:{seconds_left:02}"
        print(timer_display, end='', flush=True)
        time.sleep(1)
        duration -= 1

    print("\nTime's up! Slowly open your eyes.")
    user_data['progress'].append({
        'type': 'timer',
        'date': datetime.now().isoformat(),
        'duration': minutes
    })

    update_streak()

# View meditation progress
def view_progress():
    if not user_data['progress']:
        print("No progress yet. Start meditating today!")
        return

    print("\nMeditation Progress")
    for entry in user_data['progress']:
        if entry['type'] == 'guided':
            print(f"Guided meditation on {entry['date']}")
        elif entry['type'] == 'timer':
            print(f"Timer meditation on {entry['date']} for {entry['duration']} minutes")

# Log mood before meditation
def log_mood():
    mood = input("How do you feel before meditation? ")
    user_data['mood_log'].append({
        'date': datetime.now().isoformat(),
        'mood': mood
    })
    print("Mood logged successfully.")

# Customize guided meditation session
def customize_session():
    print("\nCustomize Your Guided Meditation Session")
    prompts = []
    while True:
        prompt = input("Enter a prompt (or type 'done' to finish): ")
        if prompt.lower() == 'done':
            break
        prompts.append(prompt)
    
    custom_session = {
        'prompts': prompts,
        'date': datetime.now().isoformat()
    }
    
    with open('custom_sessions.json', 'a') as f:
        json.dump(custom_session, f, indent=4)
    
    print("Custom session saved.")

# View meditation statistics
def view_statistics():
    total_time = sum(entry.get('duration', 0) for entry in user_data['progress'])
    session_count = len(user_data['progress'])
    average_time = total_time / session_count if session_count else 0
    streak = user_data['streak']
    
    print("\nMeditation Statistics")
    print(f"Total meditation time: {total_time} minutes")
    print(f"Average session length: {average_time:.2f} minutes")
    print(f"Current meditation streak: {streak} days")

# Update meditation streak
def update_streak():
    today = datetime.now().date()
    last_date = user_data.get('last_meditation_date')
    
    if last_date:
        last_date = datetime.strptime(last_date, '%Y-%m-%d').date()
        if (today - last_date).days == 1:
            user_data['streak'] += 1
        elif (today - last_date).days > 1:
            user_data['streak'] = 1
    else:
        user_data['streak'] = 1

    user_data['last_meditation_date'] = today.isoformat()

if __name__ == "__main__":
    main_menu()
