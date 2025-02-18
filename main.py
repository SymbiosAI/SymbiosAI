def symbios_ai():
    print("^-^ Välkommen till SymbiosAI!")
    print("Skriv 'exit' för att avsluta.\n")

    while True:
        user_input = input("^-^ Du: ")
        if user_input.lower() == "exit":
            print("^-^ SymbiosAI stängs ner...")
            break
        response = process_input(user_input)
        print(f"^-^ SymbiosAI: {response}")
def process_input(text):
    text = text.lower()
    if "hej" in text or "hallå" in text:
        return "Hej! Hur kan jag hjälpa dig idag?"
    elif "hur mår du" in text:
        return "Jag är en AI, så jag har inga känslor – men jag är redo att hjälpa dig!"
    elif "vad är symbiosai" in text:
        return "SymbiosAI är en självförsörjande AI för forskning och utveckling!"
    elif "vad kan du göra" in text:
        return "Just nu kan jag prata med dig, men jag utvecklas hela tiden!"
    elif "exit" in text:
        return "Stänger ner SymbiosAI..."
    else:
        return f"Jag hörde dig säga: '{text}', men jag vet inte hur jag ska svara på det än."




if __name__ == "__main__":
    symbios_ai()

