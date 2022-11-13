import requests
from json import loads
from time import sleep
from random import choice
from pyuseragents import random as random_useragent
import cloudscraper
from requests.exceptions import ConnectionError
from json.decoder import JSONDecodeError
import easygui as gui

from Loging import Logs


class Post:
    def __call__(self, name, tg_user, email, ref, proxy=''):
        proxy_ = {'http': proxy,
                  'https': proxy}
        headers = {
            'authority': 'app.viral-loops.com',
            'accept': '*/*',
            'accept-language': 'ru',
            # Already added when you pass json=
            # 'content-type': 'application/json',
            'origin': 'https://www.getprimal.com',
            'referer': 'https://www.getprimal.com/',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': random_useragent(),
            'x-ucid': 'SjLem5WLEHKTaPwS4MNhXFGAxew',
        }

        json_data = {
            'params': {
                'event': 'registration',
                'captchaJWT': None,
                'user': {
                    'firstname': name,
                    'lastname': tg_user,
                    'email': email,
                },
                'referrer': {
                    'referralCode': ref,
                },
                'refSource': 'copy',
                'acquiredFrom': 'form_widget',
            },
            'publicToken': 'SjLem5WLEHKTaPwS4MNhXFGAxew',
        }
        scraper = cloudscraper.create_scraper()
        scraper.headers.update(headers)
        try:
            if proxy:
                r = scraper.post('https://app.viral-loops.com/api/v2/events', json=json_data, proxies=proxy_)
            else:
                r = scraper.post('https://app.viral-loops.com/api/v2/events', json=json_data)
            return loads(r.text)['referralCode']
        except ConnectionError as error:
            Logs.log(f'error Connection -> {error}')
            raise ConnectionError('Error post conection')
        except KeyError:
            return
        except JSONDecodeError as error:
            Logs.log(f'json error -> {error}')
            raise error


class Primal:
    def __init__(self, *args):
        self.referral = args[0]
        self.num = args[1]
        self.proxy = args[2]

    @staticmethod
    def creat_email():
        return "".join([choice("abcdefghijklmnopqrstuvwxyz") for _ in range(5)]) +\
               "".join([choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(5)]) + '@gmail.com'

    @staticmethod
    def tg_users():
        users = []
        with open('channel_users.json', mode='r', encoding='UTF-8') as file:
            file = file.read()
            file = loads(file)
            try:
                for i in range(len(file)):
                    if file[i]['user'] is None:
                        del file[i]
                    else:
                        users.append('@' + file[i]['user'])
            except:
                pass
        return users

    @staticmethod
    def get_username(length):
        usernames = []

        while len(usernames) < length:
            try:
                r = requests.get('https://story-shack-cdn-v2.glitch.me/generators/username-generator')
                usernames.append(loads(r.text)['data']['name'])
            except:
                pass

        return usernames

    def run(self):
        post = Post()
        name = self.get_username(self.num)
        tg_user = self.tg_users()
        for i in range(self.num):
            if self.proxy:
                try:
                    proxy = self.proxy[i]
                except IndexError:
                    proxy = ''
            else:
                proxy = ''
            post(name[i], tg_user[i], self.creat_email(), self.referral, proxy)
            print(f'referal № {i + 1} for {self.num}')
            sleep(5)

    @staticmethod
    def ref():
        try:
            num = int(gui.enterbox(msg='How many refs are needed'))
        except TypeError:
            raise TypeError('Enter an integer')
        refs = gui.enterbox(msg='Enter your referral link')
        if len(refs) != 27:
            raise 'Error ref links'
        if len(refs) > 7:
            refs = refs.split('/')[3]
        proxy = gui.buttonbox(msg='To use HTTP Basic Auth with your proxy, use the'
                                  ' http://user:password@host.com/', choices=['YES', 'NO'])
        if proxy == 'YES':
            proxy_file = gui.fileopenbox(title='Select a file')
            with open(proxy_file, 'r') as file:
                proxy_list = file.read().splitlines()
        else:
            proxy_list = ''
        return refs, num, proxy_list


if __name__ == '__main__':
    prim = Primal(*Primal.ref())
    prim.run()

