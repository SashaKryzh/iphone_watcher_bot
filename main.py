from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup


class Watcher(ABC):
    @abstractmethod
    def is_available(self):
        pass


class RTVWatcher(Watcher):
    def __init__(self, url: str):
        self.url = url

    def is_available(self) -> bool:
        try:
            response = requests.get(self.url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            product_status_div = soup.find('div', class_='product-status')
            buttons = product_status_div.find_all('button', attrs={'data-family': 'cta--button'})
            
            for button in buttons:
                data_test = button.get('data-test')
                if data_test == 'add-product-to-the-cart':
                    return True
                
            return False

        except requests.exceptions.RequestException as e:
            raise Exception(f'Unable to check available on {self.url}: {e}')



def main():
    rtv = RTVWatcher(
        url='https://www.euro.com.pl/telefony-komorkowe/apple-iphone-15-pro-256gb-silver.bhtml'
    )
    print(rtv.is_available())
    rtv = RTVWatcher(
        url='https://www.euro.com.pl/telefony-komorkowe/apple-iphone-15-pro-256gb-gold.bhtml'
    )
    print(rtv.is_available())


if __name__ == '__main__':
    main()
