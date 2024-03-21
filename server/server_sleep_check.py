import requests
import time

while True:
    requests.get('https://review-trustyfox.pythonanywhere.com/media/sleep_check')
    requests.get('http://192.168.1.11:5000/media/sleep_check')
    time.sleep(600)
