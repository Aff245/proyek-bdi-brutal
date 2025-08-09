import requests
import json
import os
from datetime import datetime

class PlatformCoordinator:
    def __init__(self, config):
        self.config = config.get('integration', {})
        self.vercel_url = self.config.get('vercel_url')
        self.github_repo = self.config.get('github_repository')
        self.github_token = os.getenv('GITHUB_TOKEN')

    def update_vercel_status(self, component, status, metrics={}):
        if not self.vercel_url:
            print("[Koordinator] URL Vercel tidak ada, update dibatalkan.")
            return False
        
        try:
            url = f"{self.vercel_url}/api/status"
            payload = { "component": component, "status": status, "data": metrics }
            print(f"[Koordinator] Mengirim status ke Vercel: {payload}")
            # Tambahkan timeout yang lebih panjang
            response = requests.post(url, json=payload, timeout=20)
            
            if response.status_code == 200:
                print(f"[Koordinator] Status '{component}' BERHASIL dikirim ke Vercel.")
                return True
            else:
                print(f"[Koordinator] WARNING: Gagal kirim status ke Vercel (Status: {response.status_code})")
                return False
        except requests.exceptions.RequestException as e:
            print(f"[Koordinator] WARNING: Koneksi ke Vercel gagal: {e}")
            return False

    def trigger_github_workflow(self):
        if not self.github_repo or not self.github_token:
            print("[Koordinator] Repo/Token GitHub tidak ada, pemicuan dibatalkan.")
            return False

        url = f"https://api.github.com/repos/{self.github_repo}/dispatches"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.github_token}"
        }
        data = {"event_type": "quantum-processing-trigger"}

        try:
            print(f"[Koordinator] Memicu Workflow di {self.github_repo}...")
            response = requests.post(url, headers=headers, json=data, timeout=20)
            if response.status_code == 204:
                print("[Koordinator] Sinyal ke Otak Kuantum BERHASIL!")
                return True
            else:
                print(f"[Koordinator] GAGAL memicu GitHub: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"[Koordinator] Error koneksi ke GitHub: {e}")
            return False
