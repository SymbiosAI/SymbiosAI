import os
import shutil
import logging
import subprocess

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class SelfUpgrade:
    def __init__(self, file_to_upgrade="main.py", backup_dir="backups"):
        self.file_to_upgrade = file_to_upgrade
        self.backup_dir = backup_dir
        self.new_code = None

        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def backup_current_code(self):
        """ Skapar en backup av den nuvarande koden. """
        backup_path = os.path.join(self.backup_dir, f"backup_{self.file_to_upgrade}")
        shutil.copy(self.file_to_upgrade, backup_path)
        logging.info(f"✅ Backup skapad: {backup_path}")

    def read_current_code(self):
        """ Läser in den nuvarande koden. """
        with open(self.file_to_upgrade, "r", encoding="utf-8") as file:
            return file.readlines()

    def analyze_code(self, current_code):
        """ Simulerar en AI-driven analys av koden. Här kan vi lägga in en AI som föreslår förbättringar. """
        logging.info("🔍 Analyserar koden för förbättringar...")

        # Här kan en AI-modell (GPT, Llama, etc.) analysera koden och föreslå ändringar
        # För nu, gör vi en enkel ändring som ett exempel
        improved_code = []
        for line in current_code:
            if "DEBUG" in line:
                line = line.replace("DEBUG", "INFO")  # Exempel: Justera loggnivåer
            improved_code.append(line)

        self.new_code = "".join(improved_code)

    def test_new_code(self):
        """ Testar om den nya koden fungerar innan den implementeras. """
        test_file = "test_main.py"
        with open(test_file, "w", encoding="utf-8") as file:
            file.write(self.new_code)

        try:
            result = subprocess.run(["python", "-m", "py_compile", test_file], capture_output=True, text=True)

            if result.returncode == 0:
                logging.info("✅ Test av ny kod lyckades!")
                return True
            else:
                logging.error(f"❌ Test av ny kod misslyckades: {result.stderr}")
                return False
        except Exception as e:
            logging.error(f"❌ Testning avbröts p.g.a. fel: {e}")
            return False
        finally:
            os.remove(test_file)  # Ta bort testfilen efter testet

    def upgrade_code(self):
        """ Ersätter den gamla koden med den nya om den klarar testningen. """
        if self.new_code and self.test_new_code():
            with open(self.file_to_upgrade, "w", encoding="utf-8") as file:
                file.write(self.new_code)
            logging.info("🚀 Uppgraderingen lyckades! Den nya koden har implementerats.")
        else:
            logging.warning("⚠️ Uppgraderingen avbröts. Behåller den gamla koden.")

if __name__ == "__main__":
    upgrader = SelfUpgrade()
    upgrader.backup_current_code()
    current_code = upgrader.read_current_code()
    upgrader.analyze_code(current_code)
    upgrader.upgrade_code()
