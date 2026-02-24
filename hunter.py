import requests
from bs4 import BeautifulSoup
import json

class DeepA11yHunter:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.jobs = []

    def log(self, portal):
        print(f"🔍 Extrayendo vacantes reales de: {portal}...")

    def fetch_remotive(self):
        self.log("Remotive")
        try:
            res = requests.get("https://remotive.com/api/remote-jobs?search=accessibility", timeout=10).json()
            for j in res.get('jobs', []):
                self.jobs.append({
                    "title": j['title'], 
                    "company": j['company_name'], 
                    "url": j['url'], 
                    "source": "Remotive", 
                    "type": "USD / Remote"
                })
        except: pass

    def fetch_weworkremotely(self):
        self.log("WeWorkRemotely")
        try:
            res = requests.get("https://weworkremotely.com/remote-jobs/search?term=accessibility", headers=self.headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            for item in soup.select('.job-list-item')[:10]:
                title = item.select_one('.title').text.strip()
                company = item.select_one('.company').text.strip()
                link = "https://weworkremotely.com" + item.select_one('a')['href']
                self.jobs.append({"title": title, "company": company, "url": link, "source": "WWR", "type": "Contractor"})
        except: pass

    def fetch_a11yjobs(self):
        self.log("A11yJobs")
        try:
            res = requests.get("https://a11yjobs.com", headers=self.headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            for card in soup.select('.job-card')[:10]:
                title = card.select_one('.job-title').text.strip()
                company = card.select_one('.company-name').text.strip()
                link = "https://a11yjobs.com" + card.select_one('a')['href']
                self.jobs.append({"title": title, "company": company, "url": link, "source": "A11yJobs", "type": "Niche"})
        except: pass

    def fetch_linkedin_direct(self):
        self.log("LinkedIn")
        try:
            # Versión simplificada para evadir el bloqueo de login
            url = "https://www.linkedin.com/jobs/search?keywords=Accessibility&location=Remote&f_TPR=r604800"
            res = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            for job in soup.select('.base-card')[:10]:
                title = job.select_one('.base-search-card__title').text.strip()
                company = job.select_one('.base-search-card__subtitle').text.strip()
                link = job.select_one('a')['href'].split('?')[0]
                self.jobs.append({"title": title, "company": company, "url": link, "source": "LinkedIn", "type": "Global"})
        except: pass

    def save(self):
        # Limpieza de duplicados
        unique_jobs = {j['url']: j for j in self.jobs}.values()
        with open('jobs_data.json', 'w', encoding='utf-8') as f:
            json.dump(list(unique_jobs), f, indent=4, ensure_ascii=False)
        print(f"✨ Éxito: {len(unique_jobs)} vacantes específicas encontradas.")

hunter = DeepA11yHunter()
hunter.fetch_remotive()
hunter.fetch_weworkremotely()
hunter.fetch_a11yjobs()
hunter.fetch_linkedin_direct()
# Puedes seguir añadiendo funciones similares para los otros 16 portales
hunter.save()
