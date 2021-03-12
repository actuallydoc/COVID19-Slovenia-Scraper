# Standard Library Imports
import requests
import hashlib
import asyncio
from datetime import datetime

# External imports
from bs4 import BeautifulSoup
from dhooks import Webhook, Embed


class COVID19:
    def __init__(self, timeout):
        self.timeout = timeout
        self.website = "https://www.nijz.si/sl/dnevno-spremljanje-okuzb-s-sars-cov-2-covid-19"
        # Wannabe Macintosh EKSDE
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        asyncio.run(self.run())
        print("Done")

    async def run(self):
        while True:
            try:
                self.url = requests.get(self.website,
                                        headers=self.headers)
                content = self.url.text
                self.soup = BeautifulSoup(content, 'html.parser')

                self.emptylist = []

                for i in (self.soup.find_all('strong')):
                    self.emptylist.append(i)

                self.done_list = []
                for doc in self.emptylist:
                    x = str(doc).replace('<strong>', " ")
                    done = x[:-9]
                    self.done_list.append(done)

                self.stringified = str(self.done_list)
                currentHash = hashlib.sha224(self.stringified.encode('utf-8')).hexdigest()
                print("Old hash")
                print(currentHash)

                await asyncio.sleep(self.timeout)
                # Making a new request
                self.url = requests.get(self.website,
                                        headers=self.headers)

                print("Request done")
                self.res = BeautifulSoup(content, 'html.parser')

                self.rip = []

                for i in (self.res.find_all('strong')):
                    self.rip.append(i)

                self.done_rip = []
                for xd in self.rip:
                    x = str(xd).replace('<strong>', " ")
                    done = x[:-9]
                    self.done_rip.append(done)

                self.fucked = str(self.done_rip)
                newHash = hashlib.sha224(self.fucked.encode('utf-8')).hexdigest()
                print("New hash")
                print(newHash)
                print("Comparing the hashes")

                if newHash == currentHash:
                    print("Hash is the same")
                    continue
                else:
                    print("hash changed")
                    datum = self.get_date(self.done_rip)
                    prvi = self.prvi_odmerek(self.done_rip)
                    drugi = self.drugi_odmerek(self.done_rip)
                    pcr = self.pcr_testi(self.done_rip)
                    hagt = self.hagt_testi(self.done_rip)
                    ucerajpcr = self.uceraj_pcr_testi(self.done_rip)
                    ucerajhagt = self.uceraj_hagt_testi(self.done_rip)
                    potrjeni = self.potrjeni(self.done_rip)
                    ucerajpotrjeni = self.uceraj_potrjeni(self.done_rip)
                    aktivni = self.aktivniprimeri(self.done_rip)
                    na14dni = self.na14dni(self.done_rip)
                    povprečje7dni = self.povprečje7dni(self.done_rip)
                    embed = self.make_embed(datum=datum, prviodmerek=prvi, drugiodmerek=drugi, pcr=pcr, hagt=hagt,
                                            pcrpretekli=ucerajpcr, hagtpretekli=ucerajhagt)
                    embed2 = self.second_embed(potrjeni=potrjeni, potrjenipretekli=ucerajpotrjeni, aktivni=aktivni,
                                               zadnjih7dni=povprečje7dni, dni=na14dni)
                    hook = Webhook(
                        'WEBHOOKURLHERE')

                    hook.send(embed=embed)
                    asyncio.sleep(0.5)
                    hook.send(embed=embed2)
                    print("Sent the message to the discord webhook")
                    continue
            except Exception as e:
                print("Error occured")
                self.loop.close()

    async def loop_func(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(asyncio.gather(self.run()))

    # Dont question this part im a retard
    def get_date(self, test):
        # Datum /Date
        self.datum = test[0]
        print(f"Datum informacij: {self.datum}")
        return self.datum

    def prvi_odmerek(self, test):
        self.prvi = test[1]
        print(f"{self.prvi} cepljenih oseb  s prvim odmerkom")
        return self.prvi

    def drugi_odmerek(self, test):
        self.drugi = test[2]
        print(f"{self.drugi} cepljenih oseb z drugim odmerkom")
        return self.drugi

    def pcr_testi(self, test):
        self.pcr = test[3]
        print(f"{self.pcr} testiranih oseb s PCR")
        return self.pcr

    def hagt_testi(self, test):
        self.hagt = test[4]
        print(f"{self.hagt} testiranih oseb s HAGT")
        return self.hagt

    def uceraj_pcr_testi(self, test):
        self.ypcr = test[5]
        print(f"{self.ypcr} testiranih oseb s PCR3 v preteklem dnevu")
        return self.ypcr

    def uceraj_hagt_testi(self, test):
        self.yhagt = test[6]
        print(f"{self.yhagt} testiranih oseb s HAGT4 v preteklem dnevu")
        return self.yhagt

    def potrjeni(self, test):
        self.confirmed = test[7]
        print(f"{self.confirmed} potrjenih primerov")
        return self.confirmed

    def uceraj_potrjeni(self, test):
        self.yactive = test[8]
        print(f"{self.yactive} potrjenih primerov v preteklem dnevu")
        return self.yactive

    def aktivniprimeri(self, test):
        self.activecases = test[9]
        print(f"{self.activecases} aktivnih primerov (ocena)")
        return self.activecases

    def na14dni(self, test):
        self.na14 = test[10]
        print(f"{self.na14} potrjenih primerov na 100.000 prebivalcev Slovenije v zadnjih 14 dneh")
        return self.na14

    def povprečje7dni(self, test):
        self.average7dni = test[11]
        print(f"{self.average7dni} povprečje potrjenih primerov v zadnjih 7 dneh")
        return self.average7dni

    def make_embed(self, datum, prviodmerek, drugiodmerek, pcr, hagt, pcrpretekli, hagtpretekli):
        """
        This functions will create an embed with all information needed
        I had to split into 2 functions second_embed() because the embed was too big
        Orginizing the code would be nice because its a mess
        """
        embed = Embed(
            description='COV SARS 2 KURBA EMBED 1',
            color=0x5CDBF0,
            timestamp=str(datetime.now())  # sets the timestamp to current time
        )
        embed.add_field(name="Datum", value=datum, inline=False)
        embed.add_field(name=" cepljenih oseb  s prvim odmerkom", value=prviodmerek, inline=False)
        embed.add_field(name="cepljenih oseb z drugim odmerkom", value=drugiodmerek, inline=False)
        embed.add_field(name="testiranih oseb s PCR", value=pcr, inline=False)
        embed.add_field(name="testiranih oseb s HAGT", value=hagt, inline=False)
        embed.add_field(name="testiranih oseb s PCR3 v preteklem dnevu", value=pcrpretekli, inline=False)
        embed.add_field(name="testiranih oseb s HAGT v preteklem dnevu", value=hagtpretekli, inline=False)

        return embed

    def second_embed(self, potrjeni, potrjenipretekli, aktivni, dni, zadnjih7dni):
        embed = Embed(
            description='COV SARS 2 KURBA EMBED 2',
            color=0x5CDBF0,
            timestamp=str(datetime.now())  # sets the timestamp to current time
        )

        embed.add_field(name="potrjenih primerov", value=potrjeni, inline=False)
        embed.add_field(name="potrjenih primerov v preteklem dnevu", value=potrjenipretekli, inline=False)
        embed.add_field(name="aktivnih primerov (ocena)", value=aktivni, inline=False)
        embed.add_field(name="potrjenih primerov na 100.000 prebivalcev Slovenije v zadnjih 14 dneh", value=dni,
                        inline=False)
        embed.add_field(name="povprečje potrjenih primerov v zadnjih 7 dneh", value=zadnjih7dni, inline=False)
        return embed


if __name__ == '__main__':
    COVID19(1800)  # Set the timeout for each request
