#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import csv
import sys
from random import uniform, randint

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


GECKODRIVER_PATH = 'C:\\Users\\artem\\AppData\\Local\\Programs\\Python\\Python38\\Scripts\\geckodriver.exe'  # указать путь к веб-драйверу FF'а
SEARCH_QUERY = ['https://news.mail.ru/politics/' ,'https://news.mail.ru/economics/' ,'https://news.mail.ru/society/','https://news.mail.ru/incident/']# указать поисковой запрос


def get_driver():
	options = Options()#создание класса Options
	options.add_argument('--headless')  # закомментировать, чтобы в процессе выполнения открылось окно браузера

	driver = Firefox(
		options=options,
		executable_path=GECKODRIVER_PATH
	)#параметры при открытии браузера FireFox

	# _driver.set_window_size(1000, 1080)

	return driver

def get_news(driver, query, count):
	driver.get(query)#перенаправляет к странице URL в параметре
	time.sleep(uniform(3, 4))#сон в случайном промежутке 1 и 2
	try:
		while (count > 0):
			driver.find_element_by_xpath("//button[@class='button margin_top_20 js-pgng_more_link']/span[1]").click()
			count = count - 1
			time.sleep(uniform(3, 4))
	except:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
	title_news = driver.find_elements_by_xpath("//div[@class='js-module']//span[@class='newsitem__title-inner']")
	news = driver.find_elements_by_xpath("//div[@class='js-module']//span[@class='newsitem__text']")
	news_time = driver.find_elements_by_xpath("//div[@class='js-module']//span[@class='newsitem__param js-ago']")
	result_title_news_str = [0] * len(news) 
	for i in range(len(news)):
		result_title_news_str[i] = [0] * 3
	index1 = int(0)
	index2 = int(0)
	index3 = int(0)
	for write_title_news in title_news:
		result_title_news_str[index1][0] = write_title_news.text
		index1 = index1 + 1
	for write_news in news:
		result_title_news_str[index2][1] = write_news.text
		index2 = index2 + 1
	for write_news_time in news_time:
		result_title_news_str[index3][2] = write_news_time.text
		index3 = index3 + 1
	return result_title_news_str


def write_csv(news):
	with open('out.csv', 'w', encoding='utf-8') as f:
		writer = csv.writer(f,delimiter = '&')
		topic = [["Название темы", "Описание темы", "Дата"]]
		for write_topic in topic:
			writer.writerow(write_topic)
		for write_news in news:
			writer.writerow(write_news)
	return 0	


def main():
	if len(sys.argv) != 3:
		print('Usage: python3 {} <count_scrolls> <topic>\n(topic: 1 - Politics; 2 - Economy; 3 - Society; 4 - Developments) '.format(sys.argv[0]))
		sys.exit(1)
	try:
		number_of_scrolls = int(sys.argv[1])
	except ValueError:
		print('number_of_scrolls: Invalid input type')
		sys.exit(1)
	try:
		number_topic = int(sys.argv[2])
		if (number_topic > 4 or number_topic < 1):
			print('number topic: Invalid number topic')
			sys.exit(1)
	except ValueError:
		print('number topic: Invalid input type')
		sys.exit(1)
		
	print('[*] Initializing webdriver... ')
	driver = get_driver()
	print('[+] Done.')

	print('[*] Collecting news... ')
	
	
	my_news = get_news(driver, SEARCH_QUERY[number_topic - 1], number_of_scrolls)
	print('[+] Done.')

		
	driver.quit()
	if my_news:
		print('[*] Creating .csv file... ')
		try:
			write_csv(my_news)
			print('[+] Done.')
		except:
			print('[-] Failure')
	else:
		print('[-] Failure: server timeout or bad search query')


if __name__ == '__main__':
	main()
