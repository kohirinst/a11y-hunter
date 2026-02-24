import requests
from bs4 import BeautifulSoup
import json
import datetime
import time

class A11yHunterPro:
    def __init__(self):
        # User-Agent más completo para evitar bloqueos
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept-Language': 'es-ES,es;q=0.9'
        }
        self.all_jobs = []

    def fetch_a11yjobs(self):
        """Extracción de A11yJobs.com (Nicho especializado)"""
        try:
            print("Buscando en A11yJobs...")
            res = requests.get("https://a11yjobs.com", headers=self.headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            # Selector actualizado para su estructura actual
            listings = soup.find_all('div', class_='job-listing') or soup.find_all('article')
            for job in listings[:15]:
                title_el = job.find('h2') or job.find('h3')
                link_el = job.find('a')
                if title_el and link_el:
                    self.all_jobs.append({
                        "title": title_el.get_text(strip=True),
                        "company": "Especialista A11y",
                        "url": "https://a11yjobs.com" + link_el['href'] if not link_el['href'].startswith('http') else link_el['href'],
                        "source": "A11yJobs",
                        "date": "Reciente"
                    })
        except Exception as e: print(f"Error A11yJobs: {e}")

    def fetch_linkedin(self):
        """LinkedIn Jobs (Global)"""
        try:
            print("Buscando en LinkedIn...")
            # Búsqueda amplia para asegurar resultados
            url = "https://www.linkedin.com/jobs/search?keywords=Accessibility%20Specialist&location=Remote&f_TPR=r604800"
            res = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            for job in soup.select('.base-card')[:15]:
                title = job.select_one('.base-search-card__title')
                company = job.select_one('.base-search-card__subtitle')
                link = job.select_one('a')
                if title and link:
                    self.all_jobs.append({
                        "title": title.get_text(strip=True),
                        "company": company.get_text(strip=True) if company else "Empresa",
                        "url": link['href'].split('?')[0],
                        "source": "LinkedIn",
                        "date": "Esta semana"
                    })
        except Exception as e: print(f"Error LinkedIn: {e}")

    def fetch_indeed_alt(self):
        """Indeed (Versión simplificada para evitar CAPTCHA)"""
        try:
            print("Buscando en Indeed...")
            url = "https://www.indeed.com/jobs?q=accessibility+engineer&fromage=7"
            res = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            for job in soup.select('.resultContent')[:10]:
                title = job.find('span', id=lambda x: x and x.startswith('jobTitle'))
                if title:
                    self.all_jobs.append({
                        "title": title.get_text(strip=True),
                        "company": "Publicado en Indeed",
                        "url": "https://www.indeed.com",
                        "source": "Indeed",
                        "date": "Ver en portal"
                    })
        except Exception as e: print(f"Error Indeed: {e}")

    def save(self):
        # Eliminar duplicados por URL
        unique_jobs = {j['url']: j for j in self.all_jobs}.values()
        with open('jobs_data.json', 'w', encoding='utf-8') as f:
            json.dump(list(unique_jobs), f, indent=4, ensure_ascii=False)

hunter = A11yHunterPro()
hunter.fetch_a11yjobs()
hunter.fetch_linkedin()
hunter.fetch_indeed_alt()
hunter.save()
