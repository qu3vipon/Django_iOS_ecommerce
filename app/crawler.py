

import requests
import os
from bs4 import BeautifulSoup
from django.core.files.uploadedfile import SimpleUploadedFile
from selenium import webdriver

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from kurly.models import Product, Image

driver = webdriver.Chrome('/home/eunbi/Desktop/Study/크롤링/chromedriver')
driver.implicitly_wait(3)

driver.get('https://www.kurly.com/shop/goods/goods_list.php?category=038')

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
my_photos = soup.select(
    '#goodsList > div.list_goods > div > ul > li:nth-child(2) > div > div > a > img '
)
print(my_photos)
print('-----------------------------------')
for photos in my_photos:
    print(photos['src'])
    photo_url = photos['src']
    basename = os.path.basename(photo_url)
    print(basename)

    response = requests.get(photo_url)
    binary_data = response.content

    file = SimpleUploadedFile(basename, binary_data)
    instance = Image.objects.create(image=file, product=Product.objects.get(pk=1))
    print(instance)
    print(instance.image)
