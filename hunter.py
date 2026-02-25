import requests
from bs4 import BeautifulSoup
import json
import random
import time

class GhostHunter:
    def __init__(self):
        # Lista de identidades para engañar a los servidores
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        ]
        self.jobs = []

    def get_headers(self):
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def log(self, portal):
        print(f"🕵️ Lanzando ataque de extracción en: {portal}...")

    def fetch_working_nomads(self):
        self.log("Working Nomads")
        try:
            url = "https://www.workingnomads.com/jobs?query=accessibility"
            res = requests.get(url, headers=self.get_headers(), timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')
            # Intentamos romper la estructura de su lista
            for job in soup.select('.job-card')[:10]:
                title = job.select_one('h2').text.strip() if job.select_one('h2') else job.select_one('a').text.strip()
                company = job.select_one('.company-name').text.strip() if job.select_one('.company-name') else "Remote Co."
                link = "https://www.workingnomads.com" + job.select_one('a')['href']
                self.jobs.append({"title": title, "company": company, "url": link, "source": "WorkingNomads", "type": "USD / Remote"})
        except: pass

    def fetch_weworkremotely(self):
        self.log("WeWorkRemotely")
        try:
            res = requests.get("https://weworkremotely.com/remote-jobs/search?term=accessibility", headers=self.get_headers())
            soup = BeautifulSoup(res.text, 'html.parser')
            for item in soup.select('li.feature') + soup.select('li[class*="job"]'):
                title_el = item.select_one('.title')
                if title_el:
                    self.jobs.append({
                        "title": title_el.text.strip(),
                        "company": item.select_one('.company').text.strip(),
                        "url": "https://weworkremotely.com" + item.select_one('a')['href'],
                        "source": "WWR",
                        "type": "Contractor"
                    })
        except: pass

    def fetch_torre(self):
        self.log("Torre.ai (API Bruteforce)")
        try:
            # Intentamos peticion directa a su endpoint de busqueda
            payload = {"query": "accessibility", "identityType": "person", "limit": 10}
            res = requests.post("https://search.torre.ai/opportunities/_search", json=payload, timeout=10)
            data = res.json()
            for r in data.get('results', []):
                self.jobs.append({
                    "title": r.get('objective', 'A11y Role'),
                    "company": r.get('organizations', [{}])[0].get('name', 'Latam Startup'),
                    "url": f"https://torre.ai/jobs/{r.get('id')}",
                    "source": "Torre",
                    "type": "Latam / USD"
                })
        except: pass

    def fetch_simplyhired(self):
        self.log("SimplyHired (Proxy Simulation)")
        try:
            url = "https://www.simplyhired.com/search?q=accessibility&fdb=7"
            res = requests.get(url, headers=self.get_headers(), timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')
            for card in soup.select('div[class*="SerpJob-jobCard"]')[:10]:
                title = card.select_one('h3').text.strip()
                company = card.select_one('span[data-testid="companyName"]').text.strip()
                self.jobs.append({"title": title, "company": company, "url": "https://www.simplyhired.com", "source": "SimplyHired", "type": "Aggregator"})
        except: pass

    def save(self):
        # Limpieza de duplicados por titulo para que no veas lo mismo
        unique = {j['title']+j['company']: j for j in self.jobs}.values()
        with open('jobs_data.json', 'w', encoding='utf-8') as f:
            json.dump(list(unique), f, indent=4, ensure_ascii=False)
        print(f"📊 Extracción completa: {len(unique)} vacantes reales listas.")

hunter = GhostHunter()
# Ejecutamos las extracciones
hunter.fetch_working_nomads()
hunter.fetch_weworkremotely()
hunter.fetch_torre()
hunter.fetch_simplyhired()
# Guardamos
hunter.save()
