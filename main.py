nano main.py
import time

def symbios_ai():
    print("🌱 Välkommen till SymbiosAI!")
    print("Skriv 'exit' för att avsluta.\n")

    while True:
        user_input = input("🟢 Du: ")
        if user_input.lower() == "exit":
            print("🔴 SymbiosAI stängs ner...")
            break
        response = process_input(user_input)
        print(f"🤖 SymbiosAI: {response}")

def process_input(text):
    return f"Jag hörde dig säga: '{text}'. Jag lär mig fortfarande!"

if __name__ == "__main__":
    symbios_ai()

