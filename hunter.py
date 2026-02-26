import requests
from bs4 import BeautifulSoup
import json
import random

class LatamHunter:
    def __init__(self):
        self.jobs = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }

    def fetch_linkedin_latam(self):
        """Busca en LinkedIn filtrando por 'Worldwide' para asegurar que acepten Latam"""
        try:
            # El parámetro 'f_WRA=true' filtra por empleos 100% remotos
            url = "https://www.linkedin.com/jobs/search?keywords=Accessibility%20Specialist&location=Worldwide&f_TPR=r604800&f_WRA=true"
            res = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            for job in soup.select('.base-card')[:15]:
                title = job.select_one('.base-search-card__title').get_text(strip=True)
                company = job.select_one('.base-search-card__subtitle').get_text(strip=True)
                link = job.select_one('a')['href'].split('?')[0]
                self.jobs.append({"title": title, "company": company, "url": link, "source": "LinkedIn", "type": "Global/Latam"})
        except: print("Error en LinkedIn Latam")

    def fetch_remotive_latam(self):
        """Remotive permite filtrar por región 'Worldwide' vía API"""
        try:
            # Buscamos específicamente los que dicen Worldwide o Americas
            res = requests.get("https://remotive.com/api/remote-jobs?search=accessibility", timeout=10).json()
            for j in res.get('jobs', []):
                region = j.get('candidate_required_location', '').lower()
                # Solo agregamos si es abierto a todo el mundo o mencione Americas/Latam
                if 'worldwide' in region or 'americas' in region or 'latam' in region:
                    self.jobs.append({
                        "title": j['title'],
                        "company": j['company_name'],
                        "url": j['url'],
                        "source": "Remotive",
                        "type": "USD / Latam OK"
                    })
        except: print("Error en Remotive Latam")

    def fetch_weworkremotely_latam(self):
        """WWR tiene muchos puestos 'Anywhere in the world'"""
        try:
            url = "https://weworkremotely.com/remote-jobs/search?term=accessibility"
            res = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            for item in soup.select('li.feature, li.job-list-item'):
                region_el = item.select_one('.region')
                region_text = region_el.get_text().lower() if region_el else ""
                if 'anywhere' in region_text or 'latam' in region_text or 'americas' in region_text:
                    self.jobs.append({
                        "title": item.select_one('.title').get_text(strip=True),
                        "company": item.select_one('.company').get_text(strip=True),
                        "url": "https://weworkremotely.com" + item.select_one('a')['href'],
                        "source": "WWR",
                        "type": "USD / Global"
                    })
        except: pass

    def save(self):
        unique_list = {j['url']: j for j in self.jobs}.values()
        with open('jobs_data.json', 'w', encoding='utf-8') as f:
            json.dump(list(unique_list), f, indent=4, ensure_ascii=False)
        print(f"✅ Filtro Latam aplicado: {len(unique_list)} vacantes encontradas.")

bot = LatamHunter()
bot.fetch_linkedin_latam()
bot.fetch_remotive_latam()
bot.fetch_weworkremotely_latam()
bot.save()
