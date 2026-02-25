import requests
from bs4 import BeautifulSoup
import json
import random

class StableHunter:
    def __init__(self):
        self.jobs = []
        # Rotamos identidades para mayor seguridad
        self.ua_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]

    def get_headers(self):
        return {'User-Agent': random.choice(self.ua_list)}

    def fetch_linkedin(self):
        """LinkedIn: El gigante. Filtramos por remoto y última semana."""
        try:
            url = "https://www.linkedin.com/jobs/search?keywords=Accessibility&location=Remote&f_TPR=r604800"
            res = requests.get(url, headers=self.get_headers(), timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            for job in soup.select('.base-card')[:12]:
                title = job.select_one('.base-search-card__title').get_text(strip=True)
                company = job.select_one('.base-search-card__subtitle').get_text(strip=True)
                link = job.select_one('a')['href'].split('?')[0]
                self.jobs.append({"title": title, "company": company, "url": link, "source": "LinkedIn", "type": "Remote/Global"})
        except: print("Error en LinkedIn")

    def fetch_remotive(self):
        """Remotive: La mejor API para pagos en USD y contratos Contractor."""
        try:
            res = requests.get("https://remotive.com/api/remote-jobs?search=accessibility", timeout=10).json()
            for j in res.get('jobs', [])[:12]:
                self.jobs.append({
                    "title": j['title'],
                    "company": j['company_name'],
                    "url": j['url'],
                    "source": "Remotive",
                    "type": "USD / Remote"
                })
        except: print("Error en Remotive")

    def fetch_a11yjobs(self):
        """A11yJobs: El portal número 1 de accesibilidad en el mundo."""
        try:
            res = requests.get("https://a11yjobs.com", headers=self.get_headers(), timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            # Buscamos los contenedores de empleos reales
            for card in soup.find_all(['div', 'article'], class_=lambda x: x and ('job' in x.lower()))[:10]:
                link_el = card.find('a')
                if link_el:
                    title = card.find(['h2', 'h3']).get_text(strip=True) if card.find(['h2', 'h3']) else "Specialist"
                    self.jobs.append({
                        "title": title,
                        "company": "Accessibility Expert",
                        "url": "https://a11yjobs.com" + link_el['href'] if not link_el['href'].startswith('http') else link_el['href'],
                        "source": "A11yJobs",
                        "type": "Niche/USD"
                    })
        except: print("Error en A11yJobs")

    def save(self):
        # Eliminamos duplicados por URL para no repetir
        clean_list = {j['url']: j for j in self.jobs}.values()
        with open('jobs_data.json', 'w', encoding='utf-8') as f:
            json.dump(list(clean_list), f, indent=4, ensure_ascii=False)
        print(f"✅ Éxito: {len(clean_list)} vacantes reales encontradas.")

# Iniciar
bot = StableHunter()
bot.fetch_linkedin()
bot.fetch_remotive()
bot.fetch_a11yjobs()
bot.save()
