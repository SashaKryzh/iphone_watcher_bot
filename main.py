from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup


class Watcher(ABC):
    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def is_available(self):
        pass


class RTVWatcher(Watcher):
    def __init__(self, url: str):
        super().__init__(url)

    def is_available(self) -> bool:
        try:
            response = requests.get(self.url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            product_status_div = soup.find('div', class_='product-status')
            buttons = product_status_div.find_all(
                'button', attrs={'data-family': 'cta--button'})

            for button in buttons:
                data_test = button.get('data-test')
                if data_test == 'add-product-to-the-cart':
                    return True

            return False

        except requests.exceptions.RequestException as e:
            raise Exception(f'Unable to check available on {self.url}: {e}')


class iSpotWatcher(Watcher):
    def __init__(self, url: str):
        super().__init__(url)

    def is_available(self) -> bool:
        try:
            response = requests.get(self.url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            shop_items = soup.find_all(
                'li', {'data-type': 'select-shop', 'data-city': 'Wrocław'})

            for shop_item in shop_items:
                availability_div = shop_item.find(
                    'div', class_='shop-availibility')
                availability_text = availability_div.get_text(
                    strip=True) if availability_div else 'Availability not found'

                if availability_text != 'Niedostępny':
                    return True

            return False

        except requests.exceptions.RequestException as e:
            raise Exception(f'Unable to check available on {self.url}: {e}')


def main():
    # rtv = RTVWatcher(
    #     url='https://www.euro.com.pl/telefony-komorkowe/apple-iphone-15-pro-256gb-silver.bhtml'
    # )
    # print(rtv.is_available())
    ispot = iSpotWatcher(
        url='https://ispot.pl/apple-iphone-15-pro-256gb-blue-titanium'
    )
    print(ispot.is_available())


if __name__ == '__main__':
    main()
