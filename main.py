import sqlite3
import re

# Skapa anslutning till databasen
conn = sqlite3.connect("symbiosai.db")
cursor = conn.cursor()

# Skapa tabeller om de inte finns
cursor.execute("""
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_input TEXT,
    ai_response TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT UNIQUE,
    relation TEXT,
    value TEXT
)
""")
conn.commit()

# Funktion för att lagra fakta
def store_fact(subject, relation, value):
    cursor.execute("INSERT OR REPLACE INTO facts (subject, relation, value) VALUES (?, ?, ?)", (subject, relation, value))
    conn.commit()
    print(f"📝 DEBUG: Sparat - {subject} {relation} {value}")

# Funktion för att hämta fakta
def recall_fact(subject):
    cursor.execute("SELECT relation, value FROM facts WHERE subject LIKE ?", (f"%{subject}%",))
    result = cursor.fetchone()
    print(f"🔍 DEBUG: Försöker hämta fakta om '{subject}', Resultat: {result}")
    return f"{subject} {result[0]} {result[1]}" if result else None

# Funktion för att spara konversationer
def save_conversation(user_input, ai_response):
    cursor.execute("INSERT INTO conversations (user_input, ai_response) VALUES (?, ?)", (user_input, ai_response))
    conn.commit()

# Funktion för att hämta de senaste konversationerna
def recall_last_conversations(limit=5):
    cursor.execute("SELECT user_input, ai_response FROM conversations ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    return "\n".join([f"- Du sa: '{row[0]}', jag svarade: '{row[1]}'" for row in rows])

# Funktion för att tolka fakta
def interpret_fact(user_input):
    pattern = re.compile(r"kom ihåg att (.*?) heter (.*?)$", re.IGNORECASE)
    match = pattern.match(user_input)
    if match:
        subject, value = match.groups()
        store_fact(subject.strip(), "heter", value.strip())
        return f"Okej, jag ska komma ihåg att {subject.strip()} heter {value.strip()}!"
    return None

print("^-^ Välkommen till SymbiosAI!")
print("Skriv 'exit' för att avsluta.\n")

while True:
    user_input = input("^-^ Du: ")

    if user_input.lower() == "exit":
        print("^-^ SymbiosAI stängs ner...")
        break

    # Kolla om användaren lär AI:n något nytt
    fact_response = interpret_fact(user_input)
    if fact_response:
        response = fact_response

    # Om användaren frågar vad något heter
    elif "vad heter" in user_input.lower():
        subject = user_input.lower().replace("vad heter ", "").strip()
        subject = subject.rstrip("?!.,")  # Ta bort frågetecken, punkter och kommatecken
        fact = recall_fact(subject)
        response = fact if fact else "Jag vet inte det än."



    # Om användaren frågar vad AI:n minns
    elif "vad minns du" in user_input.lower():
        response = "Jag minns att vi har pratat om:\n" + recall_last_conversations()

    # Om inget av ovanstående gäller
    else:
        response = f"Jag hörde dig säga: '{user_input}', men jag vet inte hur jag ska svara på det än."

    # Spara konversationen
    save_conversation(user_input, response)
    print(f"^-^ SymbiosAI: {response}")
