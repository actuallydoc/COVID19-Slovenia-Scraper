# COVID19-Slovenia-Scraper
Scrapes and sends COVID-19 information via discord webhook
This is my project nothing else if you want to help me fix the code you can 
#Im still learning


# This is a personal project maybe you can take the idea and check the code and implement it for your country covid-19 stats

# How it works?

1. Makes a requests and scrapes table information like (daily covid-19 cases etc) and makes a SHA224 hash from that information)
2. After making the hash there is a timeout when you want to check for a change of information (1 hour preferably)
3. After the timeout is over it makes another request and hashes the information the same way and if the hash is different that means the webpage information got changed 
4. If it got changed it will send a discord webhook embed
5. Thats it



