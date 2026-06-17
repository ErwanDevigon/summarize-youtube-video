#!/usr/bin/env python3
import subprocess
import time
import os
import signal
from pathlib import Path


class LlamaServerManager:
    def __init__(self, port=8080):
        self.port = port
        self.server_process = None
        self.was_already_running = False

    def is_running(self) -> bool:
        """Vérifie si llama-server tourne déjà"""
        try:
            result = subprocess.run(["lsof", "-i", f":{self.port}"], 
                                  capture_output=True, text=True, timeout=2)
            return "llama-server" in result.stdout or "llama" in result.stdout.lower()
        except:
            try:
                result = subprocess.run(["ss", "-tlnp"], capture_output=True, text=True, timeout=2)
                return f":{self.port}" in result.stdout
            except:
                return False

    def start(self):
        """Démarre le serveur si nécessaire"""
        if self.is_running():
            print("✅ llama-server déjà en cours sur le port 8080")
            self.was_already_running = True
            return True

        print("🚀 Démarrage de llama-server (Gemma-4 12B)...")
        try:
            model_path = Path("~/llama.cpp/models/LLMs/Gemma/gemma4-12b-Q4_K_M.gguf").expanduser()
            server_path = Path("~/llama.cpp/build/bin/llama-server").expanduser()

            self.server_process = subprocess.Popen([
                str(server_path),
                "-m", str(model_path),
                "--host", "0.0.0.0",
                "--port", str(self.port),
                "-ngl", "95",
                "-c", "98304",
                "--cache-type-k", "q4_0",
                "--cache-type-v", "q4_0",
                "-t", "32",
                "-fa", "on",
                "-np", "3"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            print("   Attente du démarrage (10 secondes)...")
            time.sleep(10)
            return True

        except Exception as e:
            print(f"❌ Impossible de démarrer llama-server : {e}")
            print("   Lance-le manuellement avec la commande : lma")
            return False

    def stop_if_needed(self):
        """Arrête le serveur uniquement s'il a été lancé par ce script"""
        if self.server_process and not self.was_already_running:
            print("\n🛑 Arrêt de llama-server pour libérer les ressources...")
            try:
                os.kill(self.server_process.pid, signal.SIGTERM)
                print("   Serveur arrêté avec succès.")
            except:
                print("   Impossible d'arrêter le serveur automatiquement.")


# Pour tester directement le module
if __name__ == "__main__":
    manager = LlamaServerManager()
    manager.start()
    input("Appuyez sur Entrée pour arrêter le serveur...")
    manager.stop_if_needed()
