#!/usr/bin/env python3

import urllib.request
import requests
import json
from hdwallet import HDWallet
from hdwallet.utils import is_mnemonic
from hdwallet.symbols import BTC, ETH, LTC, ZEC, DASH
import blockcypher
import os
import argparse
import time


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# intro
print(color.YELLOW + "Welcome to seedsearch.py! Let\'s hunt for some BIP39 mnemonic seed\n" + color.END)
print(color.RED + 'DISCLAIMER: ' + color.END + 'This tool works with BIP39 seed')
print('            It is intended to make searches in a quick way, but it has not to be considered exhaustive\n')

parser = argparse.ArgumentParser(description='Mnemonic seed finder')
parser.add_argument('-d', metavar='directory', type=str, required=True, help='Directory to scan')
args = parser.parse_args()
directory = args.d

blockcypherAPI = None


def add_der(sym, lang, seedl, psph, bip, coin, num, is_hardened):
    hdwallet: HDWallet = HDWallet(symbol=sym)
    hdwallet.from_mnemonic(mnemonic=seedl, passphrase=psph, language=lang)
    hdwallet.from_index(bip, hardened=True)
    hdwallet.from_index(coin, hardened=True)
    hdwallet.from_index(0, hardened=True)
    hdwallet.from_index(0)
    hdwallet.from_index(num, hardened=is_hardened)
    if bip == 44:
        return hdwallet.p2pkh_address()
    if bip == 84:
        return hdwallet.p2wpkh_address()
    if bip == 49:
        return hdwallet.p2wpkh_in_p2sh_address()


# uses custom derivation paths used by samourai wallet
def sam_der(lang, seedl, psph, mix, num, is_hardened):
    hdwallet: HDWallet = HDWallet(symbol=BTC)
    hdwallet.from_mnemonic(mnemonic=seedl, passphrase=psph, language=lang)
    hdwallet.from_index(84, hardened=True)
    hdwallet.from_index(0, hardened=True)
    # sam premix= 2147483645' postmix= 2147483646'
    hdwallet.from_index(mix, hardened=True)
    hdwallet.from_index(0)
    hdwallet.from_index(num, hardened=is_hardened)
    return hdwallet.p2wpkh_address()


# check if online or apis will not be available
def is_connected(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False


# Creates list with addresses derived in the specifued language
def btc_list_der(lang, how_many):
    btc_list = []
    # bitcoin bip44 not hardened addresses
    index = 0
    while index < how_many:
        btc_list.append(add_der(BTC, lang, checking_str, '', 44, 0, index, False))
        index += 1
    # bitcoin bip44 hardened addresses
    index = 0
    while index < how_many:
        btc_list.append(add_der(BTC, lang, checking_str, '', 44, 0, index, True))
        index += 1
    # bitcoin bip49 not hardened addresses
    index = 0
    while index < how_many:
        btc_list.append(add_der(BTC, lang, checking_str, '', 49, 0, index, False))
        index += 1
    # bitcoin bip49 hardened addresses
    index = 0
    while index < how_many:
        btc_list.append(add_der(BTC, lang, checking_str, '', 49, 0, index, True))
        index += 1
    # bitcoin bip84 not hardened addresses
    index = 0
    while index < how_many:
        btc_list.append(add_der(BTC, lang, checking_str, '', 84, 0, index, False))
        index += 1
    # bitcoin bip84 hardened addresses
    index = 0
    while index < how_many:
        btc_list.append(add_der(BTC, lang, checking_str, '', 84, 0, index, True))
        index += 1
    # sam premix= 2147483645' postmix= 2147483646'
    index = 0
    while index < how_many:
        btc_list.append(sam_der(lang, checking_str, '', 2147483645, index, False))
        index += 1
    index = 0
    while index < how_many:
        btc_list.append(sam_der(lang, checking_str, '', 2147483646, index, False))
        index += 1
    return btc_list


def eth_list_der(lang, how_many):
    eth_list = []
    # ethereum bip44 not hardened addresses
    index = 0
    while index < how_many:
        eth_list.append(add_der(ETH, lang, checking_str, '', 44, 0, index, False))
        index += 1
    # ethereum bip44 hardened addresses
    index = 0
    while index < how_many:
        eth_list.append(add_der(ETH, lang, checking_str, '', 44, 0, index, True))
        index += 1
    return eth_list


def ltc_list_der(lang, how_many):
    ltc_list = []
    # litecoin bip44 not hardened addresses
    index = 0
    while index < how_many:
        ltc_list.append(add_der(LTC, lang, checking_str, '', 44, 0, index, False))
        index += 1
    # litecoin bip44 hardened addresses
    index = 0
    while index < how_many:
        ltc_list.append(add_der(LTC, lang, checking_str, '', 44, 0, index, True))
        index += 1
    # litecoin bip49 not hardened addresses
    index = 0
    while index < how_many:
        ltc_list.append(add_der(LTC, lang, checking_str, '', 49, 0, index, False))
        index += 1
    # litecoin bip49 hardened addresses
    index = 0
    while index < how_many:
        ltc_list.append(add_der(LTC, lang, checking_str, '', 49, 0, index, True))
        index += 1
    # litecoin bip84 not hardened addresses
    index = 0
    while index < how_many:
        ltc_list.append(add_der(LTC, lang, checking_str, '', 84, 0, index, False))
        index += 1
    # litecoin bip84 hardened addresses
    index = 0
    while index < how_many:
        ltc_list.append(add_der(LTC, lang, checking_str, '', 84, 0, index, True))
        index += 1
    return ltc_list


def dash_list_der(lang, how_many):
    dash_list = []
    # dash bip44 not hardened addresses
    index = 0
    while index < how_many:
        dash_list.append(add_der(DASH, lang, checking_str, '', 44, 0, index, False))
        index += 1
    # dash bip44 hardened addresses
    index = 0
    while index < how_many:
        dash_list.append(add_der(DASH, lang, checking_str, '', 44, 0, index, True))
        index += 1
    return dash_list


def zec_list_der(lang, how_many):
    zec_list = []
    # ethereum bip44 not hardened addresses
    index = 0
    while index < how_many:
        zec_list.append(add_der(ZEC, lang, checking_str, '', 44, 0, index, False))
        index += 1
    # ethereum bip44 hardened addresses
    index = 0
    while index < how_many:
        zec_list.append(add_der(ZEC, lang, checking_str, '', 44, 0, index, True))
        index += 1
    return zec_list


def getListOfFiles(dirName):
    # create a list of file and sub directories
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles


def check_lang(word):
    f = open('Wordlists/b39en')
    if word in f.read():
        f.close()
        return('english')
    f = open('Wordlists/b39it')
    if word in f.read():
        f.close()
        return('italian')
    f = open('Wordlists/b39cz')
    if word in f.read():
        f.close()
        return('czech')
    f = open('Wordlists/b39es')
    if word in f.read():
        f.close()
        return('spanish')
    f = open('Wordlists/b39fr')
    if word in f.read():
        f.close()
        return('french')
    f = open('Wordlists/b39pr')
    if word in f.read():
        f.close()
        return('portuguese')
    f = open('Wordlists/b39cn')
    if word in f.read():
        f.close()
        return('chinese_simplified')
    f = open('Wordlists/b39cn2')
    if word in f.read():
        f.close()
        return('chinese_traditional')
    f = open('Wordlists/b39jp')
    if word in f.read():
        f.close()
        return('japanese')
    f = open('Wordlists/b39kr')
    if word in f.read():
        f.close()
        return('korean')
    f.close()
    return ('none')


def check_word(word, language):
    if (language == 'english'):
        f = open('Wordlists/b39en')
        if word in f.read():
            f.close()
            return True
        else:
            f.close()
            return False
    if (language == 'italian'):
        f = open('Wordlists/b39it')
        if word in f.read():
            f.close()
            return True
        else:
            f.close()
            return False
    if (language == 'czech'):
        f = open('Wordlists/b39cz')
        if word in f.read():
            f.close()
            return True
        else:
            f.close()
            return False
    if (language == 'spanish'):
        f = open('Wordlists/b39es')
        if word in f.read():
            f.close()
            return True
        else:
            f.close()
            return False
    if (language == 'french'):
        f = open('Wordlists/b39fr')
        if word in f.read():
            f.close()
            return True
        else:
            f.close()
            return False
    if (language == 'portuguese'):
        f = open('Wordlists/b39pr')
        if word in f.read():
            f.close()
            return True
        else:
            f.close()
            return False
    if (language == 'chinese_simplified'):
        f = open('Wordlists/b39cn')
        if word in f.read():
            f.close()
            return True
        else:
            f.close()
            return False
    if (language == 'chinese_traditional'):
        f = open('Wordlists/b39cn2')
        if word in f.read():
            f.close()
            return True
        else:
            f.close()
            return False
    if (language == 'japanese'):
        f = open('Wordlists/b39jp')
        if word in f.read():
            f.close()
            return True
        else:
            f.close()
            return False
    if (language == 'korean'):
        f = open('Wordlists/b39kr')
        if word in f.read():
            f.close()
            return True
        else:
            f.close()
            return False


# Get the list of all files in the fiven path
listOfFiles = getListOfFiles(directory)

# Changes working directory to avoid issues with file opening
# use full path to open wordlists or full path to open files
# os.chdir('folder/with/wordlist')

temp_seed = []  # list that stores the seed during execution
seed_out = []
seed2check = []

n_files = len(listOfFiles)
print(color.BLUE + f'There are {n_files} files to scan' + color.END)
i = 0
# iterate through all the files
while i < n_files:
    # make a string with dirName + listOfFiles[i]
    f = open(listOfFiles[i], 'r')
#    print(f'checking: {listOfFiles[i]}')
    language = ''
    for line in f:   # reads the lines
        for word in line.split():
            checking = True  # used to check other wordlists if a word is not in the current wordlist
            while checking:
                if (len(temp_seed) == 0):
                    # identify language
                    language = check_lang(word)
                    if language == 'none':
                        checking = False
                    else:
                        temp_seed.append(word)
                        checking = False
                else:
                    if check_word(word, language):
                        temp_seed.append(word)
                        checking = False
                    else:
                        temp_seed = []
                if ((len(temp_seed) > 11) and (len(temp_seed) % 3 == 0)):
                    temp_seed_str = ' '.join(temp_seed)
                    # adds only valid bip39 seeds to output
                    if is_mnemonic(temp_seed_str, language):
                        langprint = language.upper()
                        # adds language of the seed (uppercase and in brackets) to the output string
                        temp_seed_str += ' (' + langprint + ')'
                        seed_out.append(temp_seed_str)
                        seed2check.append(temp_seed_str)
# Printing the output
    pr = 0
    if (len(seed_out) > 0):
        print(color.DARKCYAN + f'\n=== Seeds found in {listOfFiles[i]} ===' + color.END)
        while pr < len(seed_out):
            pr += 1
            prpr = str(pr)
            print(prpr + ' ' + seed_out[pr - 1])
    seed_out = []
    i += 1

# declaring empty lists
btc_list = []
eth_list = []
ltc_list = []
dash_list = []
zec_list = []

# SeedCheck integration
if (len(seed2check) > 0):
    tour0 = 1
    while tour0:
        print(color.BLUE + '\nDo you also want to see the addresses that could be derived with the found seeds? (y/n)' + color.END)
        ans = input()
        if ans == 'y' or ans == 'Y' or ans == 'n' or ans == 'N':
            tour0 = 0
        else:
            print(color.RED + 'Unaccepted answer! Only type y for yes or n for no' + color.END)
    if ((ans == 'y') or (ans == 'Y')):
        conn = is_connected()
        if conn:
            tour1 = 1
            while tour1:
                print(color.BLUE + 'Do you want to query public APIs to try to find out how the seeds were used? (y/n)' + color.END)
                ans2 = input()
                if ans2 == 'y' or ans2 == 'Y' or ans2 == 'n' or ans2 == 'N':
                    tour1 = 0
                else:
                    print(color.RED + 'Unaccepted answer! Only type y for yes or n for no' + color.END)
            if ((ans2 == 'y') or (ans2 == 'Y')):
                online_check = True
            else:
                online_check = False
                print(color.BLUE + 'seedsearch will work only offline' + color.END)
        else:
            print(color.RED + '\nNo internet connection, it will not be possible to check addresses online\n' + color.RED)
        prog = 0
        tour2 = 1
        while tour2:
            print(color.BLUE + 'How many addresses do you want seedsearch to derive for each derivation path (max = 10)?' + color.END)
            how_many = input()
            if how_many.isalpha():
                print(color.RED + 'Only numbers allowed' + color.END)
            else:
                tour2 = 0
        print(color.RED + 'API limits may not allow to check all the addresses' + color.END)
        how_many = int(how_many)
        if how_many > 10:
            how_many = 10
            print(color.RED + 'Limit exceeded!' + color.END)
            print('SeedSearch is going to check 10 addresses for each type to avoid overloading APIs')
        while prog < len(seed2check):
            checking_str = seed2check[prog]
            prog += 1
            checking_l = checking_str.split(' ')
            language = checking_l[-1]
            # removing brackets from language
            language = language.replace('(', '').replace(')', '').lower()
            del checking_l[-1]
            # obtaining the seed as a string without language
            checking_str = ' '.join(checking_l)
            print(color.DARKCYAN + f'\nAddresses derived with the seed:\n{checking_str}' + color.END)
            # Deriving addresses from the current seed
            btc_list = btc_list_der(language, how_many)
            eth_list = eth_list_der(language, how_many)
            ltc_list = ltc_list_der(language, how_many)
            dash_list = dash_list_der(language, how_many)
            zec_list = zec_list_der(language, how_many)
            # Printing derived addresses
            print(color.CYAN + '- Bitcoin addresses -' + color.END)
            print('BIP44')
            i = 0
            while i < len(btc_list):
                print(btc_list[i])
                i += 1
                if (i == (how_many * 2)):
                    print(' - BIP49 - ')
                elif (i == (how_many * 4)):
                    print(' - BIP84 - ')
                elif (i == (how_many * 6)):
                    print(' - SAMOURAI PREMIX ADDRESSES - ')
                elif (i == (how_many * 7)):
                    print(' - SAMOURAI POSTMIX ADDRESSES - ')
            print(color.CYAN + '\n- Ethereum addresses -' + color.END)
            i = 0
            while i < len(eth_list):
                print(eth_list[i])
                i += 1
            print(color.CYAN + '\n- Litecoin addresses -' + color.END)
            print(' - BIP44 - ')
            i = 0
            while i < len(ltc_list):
                print(ltc_list[i])
                i += 1
                if (i == (how_many * 2)):
                    print(' - BIP49 - ')
                elif (i == (how_many * 4)):
                    print(' - BIP84 - ')
            print(color.CYAN + '\n- Dash addresses -' + color.END)
            i = 0
            while i < len(dash_list):
                print(dash_list[i])
                i += 1
            print(color.CYAN + '\n- ZCash addresses -' + color.END)
            i = 0
            while i < len(zec_list):
                print(zec_list[i])
                i += 1
            if online_check == False:
                online_found = False
                print(color.RED + 'Use blockexplorers or trusted nodes to check the addresses' + color.END)
            elif online_check == True:
                online_found = False
                print(color.DARKCYAN + '\nChecking bip39 derived addresses online' + color.END)
                #check BTC
                i = 0
                while i < len(btc_list):
                    link = 'https://blockchain.info/q/addressfirstseen/' + btc_list[i]
                    used = requests.get(link)
                    data = used.text    # gives a string
                    if data != '0':
                        if i < how_many:
                            print(color.GREEN + '--- The given seed was used to derive Bitcoin addresses with derivation path m/44\'/0\'/0\'/0 ---' + color.END)
                            i = how_many
                        elif i < (how_many * 2):
                            print(color.GREEN + '--- The given seed was used to derive Bitcoin addresses with derivation path m/44\'/0\'/0\'/0\' ---' + color.END)
                            i = how_many * 2
                        elif i < (how_many * 3):
                            print(color.GREEN + '--- The given seed was used to derive Bitcoin addresses with derivation path m/49\'/0\'/0\'/0 ---' + color.END)
                            i = how_many * 3
                        elif i < (how_many * 4):
                            print(color.GREEN + '--- The given seed was used to derive Bitcoin addresses with derivation path m/49\'/0\'/0\'/0\' ---' + color.END)
                            i = how_many * 4
                        elif i < (how_many * 5):
                            print(color.GREEN + '--- The given seed was used to derive Bitcoin addresses with derivation path m/84\'/0\'/0\'/0 ---' + color.END)
                            i = how_many * 5
                        elif i < (how_many * 6):
                            print(color.GREEN + '--- The given seed was used to derive Bitcoin addresses with derivation path m/84\'/0\'/0\'/0\' ---' + color.END)
                            i = how_many * 6
                        elif i < (how_many * 7):
                            print(color.GREEN + '--- The given seed was used to derive Bitcoin addresses with Samourai PreMix derivation path m/84\'/0\'/2147483645\'/0\' ---' + color.END)
                            i = how_many * 7
                        elif i < (how_many * 8):
                            print(color.GREEN + '--- The given seed was used to derive Bitcoin addresses with Samourai PostMix derivation path m/84\'/0\'2147483646\'/0\' ---' + color.END)
                            i = how_many * 8
                        online_found = True
                    else:
                        i += 1
                # check ETH
                i = 0
                while i < len(eth_list):
                    link = 'https://api.blockcypher.com/v1/eth/main/addrs/' + eth_list[i]
                    # avoid blockcypher's limit of 3 calls per second
                    time.sleep(400/1000)
                    eth_resp = requests.get(link)
                    eth_resp = eth_resp.text
                    eth_resp_dict = json.loads(eth_resp)
                    if eth_resp_dict['n_tx'] != 0:
                        online_found = True
                        if i < how_many:
                            i = how_many
                            print(color.GREEN + '--- The given seed was used to derive Electrum addresses with derivation path m/44\'/60\'/0\'/0 ---' + color.END)
                        elif i > how_many * 2:
                            print(color.GREEN + '--- The given seed was used to derive Electrum addresses with derivation path m/44\'/60\'/0\'/0\' ---' + color.END)
                            break
                    else:
                        i += 1
                # check LTC
                i = 0
                while i < len(ltc_list):
                    ltc_tx = blockcypher.get_total_num_transactions(ltc_list[i], coin_symbol='ltc', api_key=blockcypherAPI)
                    # avoid blockcypher's limit of 3 calls per second
                    time.sleep(400/1000)
                    if ltc_tx != 0:
                        if i < how_many:
                            print(color.GREEN + '--- The given seed was used to derive Litecoin addresses with derivation path m/44\'/2\'/0\'/0 ---' + color.END)
                            i = how_many
                        elif i < (how_many * 2):
                            print(color.GREEN + '--- The given seed was used to derive Litecoin addresses with derivation path m/49\'/2\'/0\'/0 ---' + color.END)
                            i = (how_many * 2)
                        elif i < (how_many * 3):
                            print(color.GREEN + '--- The given seed was used to derive Litecoin addresses with derivation path m/84\'/2\'/0\'/0 ---' + color.END)
                            i = how_many * 3
                        elif i < (how_many * 4):
                            print(color.GREEN + '--- The given seed was used to derive Litecoin addresses with derivation path m/44\'/2\'/0\'/0\' ---' + color.END)
                            i = how_many * 4
                        elif i < (how_many * 5):
                            print(color.GREEN + '--- The given seed was used to derive Litecoin addresses with derivation path m/49\'/2\'/0\'/0\' ---' + color.END)
                            i = how_many * 5
                        elif i < (how_many * 6):
                            print(color.GREEN + '--- The given seed was used to derive Litecoin addresses with derivation path m/84\'/2\'/0\'/0\' ---' + color.END)
                            i = how_many * 6
                        online_found = True
            #            i = 18
                    else:
                        i += 1
                # Check DASH
                i = 0
                while i < len(dash_list):
                    dash_tx = blockcypher.get_total_num_transactions(dash_list[i], coin_symbol='dash', api_key=blockcypherAPI)
                    # avoid blockcypher's limit of 3 calls per second
                    time.sleep(400/1000)
                    if dash_tx != 0:
                        if i < how_many:
                            print(color.GREEN + '--- The given seed was used to derive Dash addresses with derivation path m/44\'/5\'/0\'/0 ---' + color.END)
                            i = how_many
                        elif i < (how_many * 2):
                            print(color.GREEN + '--- The given seed was used to derive Dash addresses with derivation path m/44\'/5\'/0\'/0 ---' + color.END)
                            i = how_many * 2
                        online_found = True
            #            i = 6
                    else:
                        i += 1
                # Check ZEC
                i = 0
                while i < len(zec_list):
                    link = 'https://api.zcha.in/v2/mainnet/accounts/' + zec_list[i]
                    zec_resp = requests.get(link)
                    zec_resp = zec_resp.text
                    zec_resp_dict = json.loads(zec_resp)
                    if zec_resp_dict['firstSeen'] != 0:
                        online_found = True
                        if i < how_many:
                            i = how_many
                            print(color.GREEN + '--- The given seed was used to derive ZCash addresses with derivation path m/44\'/133\'/0\'/0 ---' + color.END)
                        elif i < (how_many * 2):
                            i = how_many * 2
                            print(color.GREEN + '--- The given seed was used to derive ZCash addresses with derivation path m/44\'/133\'/0\'/0\' ---' + color.END)
                    else:
                        i += 1

            if (online_found == False and online_check == True):
                print(color.RED + '\nBip39 derivation path not found\n' + color.END)
            elif (online_found == True):
                print(color.GREEN + '\nBip39 derivation path found!\n' + color.END)
    else:
        print(color.RED + 'SeedSearch is not going to derive addresses and check them online. BYE!' + color.END)
        quit()
