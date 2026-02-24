import requests
import json
import datetime

class SuperA11yHunter:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.jobs = []
        self.keywords = ["Accessibility", "A11y", "WCAG"]

    def log(self, portal):
        print(f"📡 Rastreando: {portal}...")

    def fetch_remotive(self):
        self.log("Remotive (USD/Global)")
        try:
            res = requests.get("https://remotive.com/api/remote-jobs?search=accessibility", timeout=10).json()
            for j in res.get('jobs', []):
                self.jobs.append({"title": j['title'], "company": j['company_name'], "url": j['url'], "source": "Remotive", "type": "Remote/USD"})
        except: pass

    def fetch_weworkremotely(self):
        self.log("WeWorkRemotely (Contractor)")
        try:
            # WWR es excelente para Latam -> USA
            res = requests.get("https://weworkremotely.com/remote-jobs.rss", timeout=10)
            # Simplificado: buscando keywords en el feed
            if "Accessibility" in res.text:
                self.jobs.append({"title": "Check WWR for A11y", "company": "Various", "url": "https://weworkremotely.com/remote-jobs/search?term=accessibility", "source": "WWR", "type": "Contractor"})
        except: pass

    def fetch_torre(self):
        self.log("Torre.ai (Enfoque Latam)")
        try:
            # Torre tiene una estructura de API compleja, apuntamos al buscador directo
            self.jobs.append({"title": "Accessibility Roles en Latam", "company": "Torre.ai", "url": "https://torre.ai/search/jobs?q=accessibility", "source": "Torre", "type": "USD/Latam"})
        except: pass

    def fetch_adrz(self):
        # Agregamos acceso rápido a portales que bloquean bots pero son vitales
        portals = [
            ("A11yJobs", "https://a11yjobs.com"),
            ("LinkedIn (Remote)", "https://www.linkedin.com/jobs/search/?keywords=accessibility&f_WRA=true"),
            ("Indeed (USA/Latam)", "https://www.indeed.com/jobs?q=accessibility+remote"),
            ("Working Nomads", "https://www.workingnomads.com/jobs?query=accessibility"),
            ("FlexJobs", "https://www.flexjobs.com/search?search=accessibility"),
            ("RemoteOK", "https://remoteok.com/remote-accessibility-jobs"),
            ("Otta", "https://otta.com"),
            ("Toptal", "https://www.toptal.com/platform/talent/jobs"),
            ("Braintrust", "https://app.usebraintrust.com/jobs/"),
            ("Wellfound (AngelList)", "https://wellfound.com/role/l/accessibility-specialist/remote"),
            ("HackerNews WhoIsHiring", "https://hnhiring.com/search?q=accessibility"),
            ("Dice", "https://www.dice.com/jobs?q=accessibility&location=Remote"),
            ("SimplyHired", "https://www.simplyhired.com/search?q=accessibility&fdb=7"),
            ("Behance (Design A11y)", "https://www.behance.net/joblist?search=accessibility"),
            ("Authentic Jobs", "https://authenticjobs.com/?s=accessibility"),
            ("Dribbble Jobs", "https://dribbble.com/jobs?keywords=accessibility"),
            ("Relocate.me", "https://relocate.me/search?q=accessibility")
        ]
        for name, url in portals:
            self.jobs.append({"title": f"Revisar vacantes en {name}", "company": "Multi-Portal", "url": url, "source": name, "type": "Contractor/USD"})

    def save(self):
        with open('jobs_data.json', 'w', encoding='utf-8') as f:
            json.dump(self.jobs, f, indent=4, ensure_ascii=False)
        print(f"✅ Proceso terminado. {len(self.jobs)} fuentes listas.")

bot = SuperA11yHunter()
bot.fetch_remotive()
bot.fetch_weworkremotely()
bot.fetch_torre()
bot.fetch_adrz()
bot.save()
