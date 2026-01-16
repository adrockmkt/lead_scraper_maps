import re
import time
import requests
import tldextract
from bs4 import BeautifulSoup
from typing import List, Dict
from tenacity import retry, wait_fixed, stop_after_attempt

from config import (
    EMAIL_DOMINIOS_GENERICOS,
    EMAIL_FUNCIONAL_KEYWORDS
)

HEADERS = {
    "User-Agent": None  # será preenchido no init
}

TIMEOUT = 15
CRAWL_DELAY = 1.2

# ======================================================
# SITE CRAWLER
# ======================================================

class SiteCrawler:
    def __init__(self, user_agent: str):
        HEADERS["User-Agent"] = user_agent
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    # --------------------------------------------------
    # REQUEST COM RETRY
    # --------------------------------------------------
    @retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
    def _get(self, url: str) -> requests.Response:
        response = self.session.get(
            url,
            timeout=TIMEOUT,
            allow_redirects=True
        )
        response.raise_for_status()
        return response

    # --------------------------------------------------
    # NORMALIZA URL
    # --------------------------------------------------
    def _normalize_url(self, url: str) -> str:
        if not url.startswith("http"):
            return f"https://{url}"
        return url.rstrip("/")

    # --------------------------------------------------
    # EXTRAI EMAILS DO HTML
    # --------------------------------------------------
    def _extract_emails(self, html: str) -> List[str]:
        emails = set(
            re.findall(
                r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
                html
            )
        )
        return list(emails)

    # --------------------------------------------------
    # CLASSIFICA EMAIL
    # --------------------------------------------------
    def _classify_email(self, email: str) -> Dict:
        email = email.lower()
        domain = email.split("@")[-1]

        # genérico
        if domain in EMAIL_DOMINIOS_GENERICOS:
            return {
                "email": email,
                "tipo": "generico"
            }

        # funcional
        for keyword in EMAIL_FUNCIONAL_KEYWORDS:
            if keyword in email:
                return {
                    "email": email,
                    "tipo": "funcional"
                }

        return {
            "email": email,
            "tipo": "corporativo"
        }

    # --------------------------------------------------
    # IDENTIFICA LINKS DE CONTATO
    # --------------------------------------------------
    def _find_contact_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        links = set()

        for a in soup.find_all("a", href=True):
            href = a["href"].lower()

            if any(k in href for k in ["contato", "contact", "fale", "about"]):
                if href.startswith("http"):
                    links.add(href)
                else:
                    links.add(f"{base_url}/{href.lstrip('/')}")

        return list(links)

    # --------------------------------------------------
    # CRAWL SITE COMPLETO (LEVE)
    # --------------------------------------------------
    def crawl_site(self, site_url: str) -> Dict:
        result = {
            "emails_corporativos": [],
            "emails_genericos": []
        }

        if not site_url:
            return result

        site_url = self._normalize_url(site_url)

        try:
            response = self._get(site_url)
        except Exception:
            return result

        soup = BeautifulSoup(response.text, "lxml")

        # emails da home
        emails = self._extract_emails(response.text)

        # buscar páginas de contato
        contact_links = self._find_contact_links(soup, site_url)

        for link in contact_links:
            try:
                time.sleep(CRAWL_DELAY)
                r = self._get(link)
                emails.extend(self._extract_emails(r.text))
            except Exception:
                continue

        # classificar emails
        for email in set(emails):
            classification = self._classify_email(email)

            if classification["tipo"] == "generico":
                result["emails_genericos"].append(email)
            else:
                result["emails_corporativos"].append(email)

        return result