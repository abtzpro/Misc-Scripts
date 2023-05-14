import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

discount_websites = [
    "https://www.example1.com",
    "https://www.example2.com",
    "https://www.example3.com"
]

def scrape_discount_codes(url):
    discount_codes = []

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Adjust the scraping logic based on the website structure
        # ...

    except (requests.RequestException, ValueError, KeyError) as e:
        error_message = f"An error occurred while scraping discount codes from {url}: {e}"
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {error_message}")
        return []

    return discount_codes

def scrape_discounts():
    scraped_codes = []

    with open("Discounts.txt", "w") as file:
        for website in discount_websites:
            print(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} Scraping {website}...")
            codes = scrape_discount_codes(website)
            
            if codes:
                scraped_codes.extend(codes)
                print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Scraped {len(codes)} codes from {website}")
            else:
                print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} No codes found on {website}")

        if scraped_codes:
            file.write("Scraped Discount Codes:\n")
            file.write("\n".join(scraped_codes))
            print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Discount codes exported to Discounts.txt")
        else:
            print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} No discount codes scraped")

scrape_discounts()
