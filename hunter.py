def fetch_social_search(self):
        """Usa Google para encontrar vacantes en X e Instagram sin ser bloqueado"""
        self.log("Redes Sociales (X e Instagram via Index)")
        try:
            # Consultas específicas para redes sociales
            queries = [
                "site:x.com 'accessibility' 'hiring' 'remote'",
                "site:instagram.com 'accessibility specialist' 'hiring' 'latam'"
            ]
            
            for query in queries:
                # Usamos un buscador de respaldo que permite peticiones de bots
                url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                self.jobs.append({
                    "title": f"Búsqueda de vacantes en {query.split(':')[1].split(' ')[0]}",
                    "company": "Ver posts recientes",
                    "url": url,
                    "source": "Social Search",
                    "type": "Social Media"
                })
        except: pass
