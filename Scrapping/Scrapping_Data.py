import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

# Fungsi untuk mengambil data dari halaman O*NET dengan paginasi
def scrape_onet_personality(url, personality):
    data = []
    page = 1
    max_attempts = 30  # Batas percobaan untuk halaman

    while True:
        # Tambahkan parameter halaman ke URL
        page_url = f"{url}?p={page}" if page > 1 else url
        print(f"Scraping {personality} - Page {page}: {page_url}")
        
        try:
            response = requests.get(page_url, timeout=10)
            response.raise_for_status()  # Pastikan respons sukses
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break
        
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        
        # Jika tabel tidak ditemukan atau halaman kosong, hentikan
        if not table or "No results found" in soup.text:
            print(f"No more data for {personality} at page {page}")
            break
        
        rows = table.find_all('tr')[1:]  # Lewati header
        if not rows:  # Jika tidak ada baris data
            print(f"No rows found on page {page}")
            break
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                job_code = cols[0].text.strip()
                job_title = cols[1].text.strip()
                job_zone = cols[2].text.strip()
                
                # Ambil interest areas
                interest_areas = cols[3].text.strip().split(', ')
                first_interest = interest_areas[0] if len(interest_areas) > 0 else None
                second_interest = interest_areas[1] if len(interest_areas) > 1 else None
                third_interest = interest_areas[2] if len(interest_areas) > 2 else None
                
                # Cek apakah ditampilkan di "Fewer Occupations"
                shown_fewer = 'Yes' if 'Show fewer occupations' in cols[3].text else None
                
                data.append({
                    'O*NET-SOC Code': job_code,
                    'O*NET-SOC Title': job_title,
                    'Job Zone': job_zone,
                    'First Interest Area': first_interest,
                    'Second Interest Area': second_interest,
                    'Third Interest Area': third_interest,
                    'Shown in Fewer Occupations': shown_fewer
                })
        
        page += 1
        time.sleep(1)  # Delay untuk menghindari rate limiting
        
        # Batas maksimum halaman untuk mencegah loop tak terbatas
        if page > max_attempts:
            print(f"Reached max page limit ({max_attempts}) for {personality}")
            break
    
    return pd.DataFrame(data)

# Fungsi untuk mengambil dataset pekerjaan dengan paginasi
def scrape_onet_occupations(url):
    data = []
    page = 1
    max_attempts = 50  # Batas halaman lebih besar karena data pekerjaan banyak
    
    while True:
        page_url = f"{url}&p={page}" if page > 1 else url
        print(f"Scraping Occupations - Page {page}: {page_url}")
        
        try:
            response = requests.get(page_url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break
        
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        
        if not table or "No results found" in soup.text:
            print(f"No more data for occupations at page {page}")
            break
        
        rows = table.find_all('tr')[1:]  # Lewati header
        if not rows:
            print(f"No rows found on page {page}")
            break
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                code = cols[0].text.strip()
                occupation = cols[1].text.strip()
                job_family = cols[2].text.strip()
                
                data.append({
                    'Code': code,
                    'Occupation': occupation,
                    'Job Family': job_family
                })
        
        page += 1
        time.sleep(1)  # Delay untuk menghindari rate limiting
        
        if page > max_attempts:
            print(f"Reached max page limit ({max_attempts}) for occupations")
            break
    
    return pd.DataFrame(data)

# Link dari dokumen
riasec_urls = {
    'Realistic': 'https://www.onetonline.org/explore/interests/Realistic/',
    'Investigative': 'https://www.onetonline.org/explore/interests/Investigative/',
    'Artistic': 'https://www.onetonline.org/explore/interests/Artistic/',
    'Social': 'https://www.onetonline.org/explore/interests/Social/',
    'Enterprising': 'https://www.onetonline.org/explore/interests/Enterprising/',
    'Conventional': 'https://www.onetonline.org/explore/interests/Conventional/'
}
occupation_url = 'https://www.onetonline.org/find/family?f=0&g=Go'

# Scraping dataset RIASEC
riasec_dfs = []
for personality, url in riasec_urls.items():
    df = scrape_onet_personality(url, personality)
    print(f"Collected {len(df)} rows for {personality}")
    riasec_dfs.append(df)

# Gabungkan semua dataset RIASEC
riasec_combined = pd.concat(riasec_dfs, ignore_index=True)
riasec_combined = riasec_combined.drop_duplicates()  # Hapus duplikat jika ada

# Scraping dataset pekerjaan
occupation_df = scrape_onet_occupations(occupation_url)
occupation_df = occupation_df.drop_duplicates()  # Hapus duplikat jika ada

# Simpan ke CSV
riasec_combined.to_csv('riasec_dataset_full.csv', index=False)
occupation_df.to_csv('occupation_dataset_full.csv', index=False)

print(f"Dataset RIASEC berhasil disimpan: riasec_dataset_full.csv ({len(riasec_combined)} rows)")
print(f"Dataset Pekerjaan berhasil disimpan: occupation_dataset_full.csv ({len(occupation_df)} rows)")