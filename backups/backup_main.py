import sqlite3
import re
import logging

# Konfigurera logging för bättre felsökning
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class SymbiosAI:
    def __init__(self, db_name="symbiosai.db"):
        self.db_name = db_name
        self.setup_database()

    def get_db_connection(self):
        """ Skapar och returnerar en databasanslutning. """
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Gör att vi kan hämta data med namn istället för index
        return conn

    def setup_database(self):
        """ Skapar databastabeller om de inte redan finns. """
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
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
        logging.info("✅ Databasen är uppsatt och redo.")

    def store_fact(self, subject, relation, value):
        """ Lagrar fakta i databasen och normaliserar pronomen. """
        subject = self.normalize_subject(subject)
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO facts (subject, relation, value) VALUES (?, ?, ?)",
                    (subject, relation, value)
                )
                conn.commit()
            logging.info(f"✅ Sparat fakta: {subject} {relation} {value}")
        except sqlite3.Error as e:
            logging.error(f"❌ Fel vid lagring av fakta: {e}")

    def recall_fact(self, subject):
        """ Hämtar fakta om ett ämne och returnerar rätt svar. """
        subject = self.normalize_subject(subject)
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT relation, value FROM facts WHERE subject=?", (subject,))
            result = cursor.fetchone()
        
        if result:
            logging.info(f"🔍 Hämtade fakta: {subject} {result['relation']} {result['value']}")
            return f"{subject} {result['relation']} {result['value']}"
        else:
            return "Jag vet inte det än."

    def save_conversation(self, user_input, ai_response):
        """ Sparar en konversation i databasen. """
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO conversations (user_input, ai_response) VALUES (?, ?)",
                    (user_input, ai_response)
                )
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"❌ Fel vid lagring av konversation: {e}")

    def recall_last_conversations(self, limit=5):
        """ Hämtar de senaste konversationerna. """
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_input, ai_response FROM conversations ORDER BY id DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
        return "\n".join([f"- Du sa: '{row['user_input']}', jag svarade: '{row['ai_response']}'" for row in rows]) if rows else "Jag har ingen historik."

    def interpret_fact(self, user_input):
        """ Tolkar fakta och sparar den i databasen. """
        patterns = [
            re.compile(r"(?:kom ihåg|lär dig|memorera) att (.*?) (heter|är|betyder) (.*?)$", re.IGNORECASE),
            re.compile(r"^jag heter (.*?)$", re.IGNORECASE),
            re.compile(r"^mitt namn är (.*?)$", re.IGNORECASE),
            re.compile(r"^jag är (.*?)$", re.IGNORECASE)
        ]

        for pattern in patterns:
            match = pattern.match(user_input)
            if match:
                if len(match.groups()) == 3:
                    subject, relation, value = match.groups()
                else:
                    subject, relation, value = "du", "heter", match.group(1)

                self.store_fact(subject.strip(), relation.strip(), value.strip())
                return f"Okej, jag ska komma ihåg att {subject.strip()} {relation.strip()} {value.strip()}."

        return None




    def normalize_subject(self, subject):
        """ Normaliserar subjekt för att hantera pronomen korrekt. """
        subject = subject.lower()
        subject = subject.replace("min ", "din ").replace("mitt ", "ditt ")
        if subject == "jag":
            return "du"
        return subject

    def get_predefined_response(self, user_input):
        """ Hanterar vanliga fraser med fördefinierade svar. """
        greetings = ["hej", "hallå", "tjena", "hejsan", "god morgon", "god kväll"]
        farewells = ["hejdå", "adjö", "vi ses", "bye", "farväl"]
        how_are_you = ["hur mår du", "hur är läget", "hur står det till"]

        if any(user_input.startswith(greet) for greet in greetings):
            return "Hej! Hur kan jag hjälpa dig idag? 😊"
        elif any(user_input.startswith(bye) for bye in farewells):
            return "Hejdå! Vi ses nästa gång! 👋"
        elif any(user_input in how_are_you for user_input in user_input.split()):
            return "Jag är en AI, så jag har inga känslor, men jag är här för att hjälpa dig! 🤖"

        return None

    def handle_input(self, user_input):
        """ Hanterar en användares input och ger ett svar. """
        response = self.get_predefined_response(user_input)
        if response is None:
            response = self.interpret_fact(user_input)

        if response is None and ("vad heter" in user_input or "vad är" in user_input):
            subject = re.sub(r"(vad heter|vad är)", "", user_input, flags=re.IGNORECASE).strip()
            response = self.recall_fact(subject)

        if response is None and "vad minns du" in user_input:
            response = "Jag minns att vi har pratat om:\n" + self.recall_last_conversations()

        if response is None:
            response = f"Jag hörde dig säga: '{user_input}', men jag vet inte hur jag ska svara på det än."

        self.save_conversation(user_input, response)
        return response

def main():
    ai = SymbiosAI()
    print("🤖 Välkommen till SymbiosAI!")
    print("Skriv 'exit' för att avsluta.\n")

    while True:
        user_input = input("👤 Du: ").strip().lower()
        if user_input == "exit":
            print("👋 SymbiosAI stängs ner...")
            break

        response = ai.handle_input(user_input)
        print(f"🤖 SymbiosAI: {response}")

if __name__ == "__main__":
    main()
