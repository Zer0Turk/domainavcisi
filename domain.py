import os
import sys
import subprocess
import time
import random
import string

def setup_environment():
    required_libraries = ['python-whois', 'colorama']
    for lib in required_libraries:
        try:
            __import__(lib.replace('python-', ''))
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

setup_environment()

from colorama import Fore, Style, init
import whois

init(autoreset=True)

class DomainAvcisi:
    def __init__(self):
        self.found_domains = []
        self.filename = self.get_unique_filename("musait_domainler.txt")

    def get_unique_filename(self, basename):
        if not os.path.exists(basename):
            return basename
        
        name, ext = os.path.splitext(basename)
        counter = 1
        while os.path.exists(f"{name}({counter}){ext}"):
            counter += 1
        return f"{name}({counter}){ext}"

    def banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + Style.BRIGHT + "=" * 55)
        print(Fore.YELLOW + "      CyberAkademi.Org Domain Avcısı v1.0")
        print(Fore.WHITE + f"      Kayıt Dosyası: {self.filename}")
        print(Fore.CYAN + "=" * 55 + "\n")

    def generate_random_domain(self, length, tld, only_letters):
        pool = string.ascii_lowercase if only_letters else string.ascii_lowercase + string.digits
        name = ''.join(random.choice(pool) for _ in range(length))
        return f"{name}.{tld}"

    def check_availability(self, domain):
        try:
            w = whois.whois(domain)
            if not w.domain_name:
                return True
            return False
        except Exception as e:
            if "timed out" in str(e).lower():
                print(Fore.RED + f"\n[!] Sunucu yoğun (Timeout), 2 sn dinleniliyor...")
                time.sleep(2)
                return False
            return True

    def start_hunting(self):
        self.banner()
        
        tld = input(Fore.GREEN + "[?] Hangi uzantıyı taramak istersiniz? (com/net/org/xyz): ").strip().replace(".", "")
        
        try:
            length = int(input(Fore.GREEN + "[?] Domain kaç karakterli olsun? (Örn: 4): ").strip())
        except:
            length = 5

        only_letters = input(Fore.GREEN + "[?] Sadece harf mi olsun? (e/h): ").strip().lower() == 'e'

        try:
            limit = int(input(Fore.GREEN + "[?] Kaç adet deneme yapılsın?: ").strip())
        except:
            limit = 10

        print(Fore.MAGENTA + f"\n[*] {limit} adet deneme başlatılıyor...")
        print(Fore.MAGENTA + f"[*] Sonuçlar '{self.filename}' dosyasına yazılacak.\n")
        
        count = 0
        while count < limit:
            domain = self.generate_random_domain(length, tld, only_letters)
            print(Fore.WHITE + f"[*] Kontrol ediliyor: {domain}          ", end="\r")
            
            if self.check_availability(domain):
                print(Fore.GREEN + f"[+] MÜSAİT: {domain}          ")
                self.found_domains.append(domain)
                with open(self.filename, "a", encoding="utf-8") as f:
                    f.write(domain + "\n")
            
            count += 1
            time.sleep(0.8)

        print(Fore.CYAN + "\n" + "=" * 55)
        print(Fore.YELLOW + " TARAMA TAMAMLANDI!")
        print(Fore.WHITE + f" Bulunan Toplam Domain: {len(self.found_domains)}")
        print(Fore.WHITE + f" Kaydedilen Dosya      : {os.path.abspath(self.filename)}")
        print(Fore.CYAN + "=" * 55)
        
        input(Fore.GREEN + "\nÇıkmak için ENTER tuşuna basın...")

if __name__ == "__main__":
    avci = DomainAvcisi()
    avci.start_hunting()