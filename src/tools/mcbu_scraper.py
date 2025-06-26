"""
MCBU Web Scraper Tool
Manisa Celal Bayar Üniversitesi web sitesini scrape eder
"""

import re
import asyncio
from typing import Dict, Any, List, Optional
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

from .base_tool import BaseTool

class MCBUScraperTool(BaseTool):
    """MCBU web sitesi scraper tool'u"""
    
    def __init__(self):
        super().__init__(
            name="mcbu_web_scraper",
            description="Manisa Celal Bayar Üniversitesi web sitesini scrape eder",
            input_schema={
                "type": "object",
                "properties": {
                    "page_type": {
                        "type": "string",
                        "enum": [
                            "vizyon_misyon",
                            "fakulteler",
                            "bolumler", 
                            "akademik_takvim",
                            "yonetim",
                            "iletisim",
                            "ogrenci_isleri",
                            "custom_url"
                        ],
                        "description": "Scrape edilecek sayfa türü"
                    },
                    "custom_url": {
                        "type": "string",
                        "description": "Özel URL (page_type=custom_url için gerekli)"
                    },
                    "fakulte_id": {
                        "type": "string", 
                        "description": "Fakülte ID'si (bölümler için)"
                    },
                    "max_content_length": {
                        "type": "integer",
                        "default": 5000,
                        "description": "Maksimum içerik uzunluğu"
                    }
                },
                "required": ["page_type"]
            }
        )
        
        self.base_url = "https://www.mcbu.edu.tr"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """MCBU web sitesini scrape et"""
        page_type = kwargs.get("page_type")
        custom_url = kwargs.get("custom_url")
        fakulte_id = kwargs.get("fakulte_id")
        max_length = kwargs.get("max_content_length", 5000)
        
        try:
            if page_type == "vizyon_misyon":
                result = await self._scrape_vizyon_misyon()
            elif page_type == "fakulteler":
                result = await self._scrape_fakulteler()
            elif page_type == "bolumler":
                result = await self._scrape_bolumler(fakulte_id)
            elif page_type == "akademik_takvim":
                result = await self._scrape_akademik_takvim()
            elif page_type == "yonetim":
                result = await self._scrape_yonetim()
            elif page_type == "iletisim":
                result = await self._scrape_iletisim()
            elif page_type == "ogrenci_isleri":
                result = await self._scrape_ogrenci_isleri()
            elif page_type == "custom_url":
                if not custom_url:
                    return self.create_error_response("custom_url parametresi gerekli")
                result = await self._scrape_custom_url(custom_url, max_length)
            else:
                return self.create_error_response(f"Bilinmeyen sayfa türü: {page_type}")
            
            return self.create_success_response(result, f"{page_type} başarıyla scrape edildi")
            
        except Exception as e:
            return self.create_error_response(f"Scraping hatası: {str(e)}")
    
    async def _scrape_vizyon_misyon(self) -> Dict[str, Any]:
        """Üniversitenin vizyon ve misyon bilgilerini scrape et"""
        url = f"{self.base_url}/kurumsal/vizyon-misyon"
        
        response = await self._get_page(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Vizyon ve misyon içeriklerini bul
        content = {}
        
        # Sayfa başlığı
        title = soup.find('h1') or soup.find('title')
        if title:
            content['sayfa_basligi'] = title.get_text().strip()
        
        # Ana içerik
        main_content = soup.find('div', class_='content') or soup.find('main') or soup.find('article')
        if main_content:
            # Metni temizle
            text = self._clean_text(main_content.get_text())
            content['icerik'] = text
            
            # Vizyon ve misyon bölümlerini ayır
            sections = self._extract_sections(text)
            content.update(sections)
        
        content['url'] = url
        return content
    
    async def _scrape_fakulteler(self) -> Dict[str, Any]:
        """Fakülte listesini scrape et"""
        url = f"{self.base_url}/fakulteler"
        
        response = await self._get_page(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        fakulteler = []
        
        # Fakülte linklerini bul
        fakulte_links = soup.find_all('a', href=re.compile(r'/fakulte/'))
        
        for link in fakulte_links:
            fakulte_info = {
                'ad': link.get_text().strip(),
                'url': urljoin(self.base_url, link.get('href')),
                'href': link.get('href')
            }
            
            # Fakülte ID'sini çıkar
            href = link.get('href', '')
            match = re.search(r'/fakulte/([^/]+)', href)
            if match:
                fakulte_info['id'] = match.group(1)
            
            fakulteler.append(fakulte_info)
        
        return {
            'fakulteler': fakulteler,
            'toplam_fakulte': len(fakulteler),
            'url': url
        }
    
    async def _scrape_bolumler(self, fakulte_id: Optional[str] = None) -> Dict[str, Any]:
        """Bölüm listesini scrape et"""
        if fakulte_id:
            url = f"{self.base_url}/fakulte/{fakulte_id}/bolumler"
        else:
            url = f"{self.base_url}/bolumler"
        
        response = await self._get_page(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        bolumler = []
        
        # Bölüm linklerini bul
        bolum_links = soup.find_all('a', href=re.compile(r'/bolum/'))
        
        for link in bolum_links:
            bolum_info = {
                'ad': link.get_text().strip(),
                'url': urljoin(self.base_url, link.get('href')),
                'href': link.get('href')
            }
            
            # Bölüm ID'sini çıkar
            href = link.get('href', '')
            match = re.search(r'/bolum/([^/]+)', href)
            if match:
                bolum_info['id'] = match.group(1)
            
            bolumler.append(bolum_info)
        
        return {
            'bolumler': bolumler,
            'toplam_bolum': len(bolumler),
            'fakulte_id': fakulte_id,
            'url': url
        }
    
    async def _scrape_akademik_takvim(self) -> Dict[str, Any]:
        """Akademik takvim bilgilerini scrape et"""
        url = f"{self.base_url}/akademik/akademik-takvim"
        
        response = await self._get_page(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Takvim tablolarını bul
        tables = soup.find_all('table')
        takvim_verileri = []
        
        for table in tables:
            rows = table.find_all('tr')
            table_data = []
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                row_data = [cell.get_text().strip() for cell in cells]
                if row_data:
                    table_data.append(row_data)
            
            if table_data:
                takvim_verileri.append(table_data)
        
        # Ana içerik metni
        main_content = soup.find('div', class_='content') or soup.find('main')
        content_text = ""
        if main_content:
            content_text = self._clean_text(main_content.get_text())
        
        return {
            'takvim_tablolari': takvim_verileri,
            'icerik': content_text,
            'url': url
        }
    
    async def _scrape_yonetim(self) -> Dict[str, Any]:
        """Yönetim bilgilerini scrape et"""
        url = f"{self.base_url}/kurumsal/yonetim"
        
        response = await self._get_page(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        yoneticiler = []
        
        # Yönetici kartlarını bul
        yonetici_cards = soup.find_all('div', class_=re.compile(r'card|person|yonetici'))
        
        for card in yonetici_cards:
            yonetici_info = {}
            
            # İsim
            name_elem = card.find(['h3', 'h4', 'h5', '.name'])
            if name_elem:
                yonetici_info['ad_soyad'] = name_elem.get_text().strip()
            
            # Unvan
            title_elem = card.find(['p', '.title', '.unvan'])
            if title_elem:
                yonetici_info['unvan'] = title_elem.get_text().strip()
            
            # İletişim
            email_elem = card.find('a', href=re.compile(r'mailto:'))
            if email_elem:
                yonetici_info['email'] = email_elem.get('href').replace('mailto:', '')
            
            if yonetici_info:
                yoneticiler.append(yonetici_info)
        
        return {
            'yoneticiler': yoneticiler,
            'toplam_yonetici': len(yoneticiler),
            'url': url
        }
    
    async def _scrape_iletisim(self) -> Dict[str, Any]:
        """İletişim bilgilerini scrape et"""
        url = f"{self.base_url}/iletisim"
        
        response = await self._get_page(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        iletisim_bilgileri = {}
        
        # Ana içerik
        main_content = soup.find('div', class_='content') or soup.find('main')
        if main_content:
            text = main_content.get_text()
            
            # Telefon numaralarını bul
            telefon_pattern = r'(\+90\s?)?(\d{3}[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2})'
            telefonlar = re.findall(telefon_pattern, text)
            if telefonlar:
                iletisim_bilgileri['telefonlar'] = [''.join(tel) for tel in telefonlar]
            
            # Email adreslerini bul
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text)
            if emails:
                iletisim_bilgileri['emailler'] = emails
            
            # Adres bilgilerini bul
            iletisim_bilgileri['icerik'] = self._clean_text(text)
        
        iletisim_bilgileri['url'] = url
        return iletisim_bilgileri
    
    async def _scrape_ogrenci_isleri(self) -> Dict[str, Any]:
        """Öğrenci İşleri bilgilerini scrape et"""
        url = f"{self.base_url}/ogrenci-isleri"
        
        response = await self._get_page(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ana içerik
        main_content = soup.find('div', class_='content') or soup.find('main')
        content_text = ""
        if main_content:
            content_text = self._clean_text(main_content.get_text())
        
        # Alt linkler
        sub_links = []
        links = soup.find_all('a', href=re.compile(r'ogrenci'))
        for link in links:
            if link.get_text().strip():
                sub_links.append({
                    'baslik': link.get_text().strip(),
                    'url': urljoin(self.base_url, link.get('href'))
                })
        
        return {
            'icerik': content_text,
            'alt_linkler': sub_links,
            'url': url
        }
    
    async def _scrape_custom_url(self, url: str, max_length: int) -> Dict[str, Any]:
        """Özel URL'yi scrape et"""
        response = await self._get_page(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Sayfa başlığı
        title = soup.find('title')
        page_title = title.get_text().strip() if title else ""
        
        # Ana içerik
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        if not main_content:
            main_content = soup.find('body')
        
        content_text = ""
        if main_content:
            content_text = self._clean_text(main_content.get_text())
            
            # İçerik uzunluğunu sınırla
            if len(content_text) > max_length:
                content_text = content_text[:max_length] + "..."
        
        # Linkler
        links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            text = link.get_text().strip()
            if text and href:
                full_url = urljoin(url, href)
                links.append({
                    'text': text,
                    'url': full_url
                })
        
        return {
            'sayfa_basligi': page_title,
            'icerik': content_text,
            'linkler': links[:20],  # İlk 20 link
            'url': url,
            'domain': urlparse(url).netloc
        }
    
    async def _get_page(self, url: str) -> requests.Response:
        """Sayfayı al"""
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.session.get(url, timeout=10)
            )
            response.raise_for_status()
            return response
        except Exception as e:
            raise Exception(f"Sayfa alınamadı ({url}): {e}")
    
    def _clean_text(self, text: str) -> str:
        """Metni temizle"""
        # Çoklu boşlukları tek boşluğa çevir
        text = re.sub(r'\s+', ' ', text)
        # Baş ve sondaki boşlukları kaldır
        text = text.strip()
        return text
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Metinden bölümleri çıkar (vizyon, misyon vs.)"""
        sections = {}
        
        # Vizyon
        vizyon_match = re.search(r'vizyon[:\s]*([^.]*(?:\.[^.]*){0,3})', text, re.IGNORECASE)
        if vizyon_match:
            sections['vizyon'] = vizyon_match.group(1).strip()
        
        # Misyon
        misyon_match = re.search(r'misyon[:\s]*([^.]*(?:\.[^.]*){0,3})', text, re.IGNORECASE)
        if misyon_match:
            sections['misyon'] = misyon_match.group(1).strip()
        
        # Değerler
        degerler_match = re.search(r'değer[^:]*[:\s]*([^.]*(?:\.[^.]*){0,5})', text, re.IGNORECASE)
        if degerler_match:
            sections['degerler'] = degerler_match.group(1).strip()
        
        return sections