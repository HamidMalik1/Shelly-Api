import csv, urllib.request

url = 'http://ilmanet.fi/download.php?orderId=93173&id=127&type=solar&limit=1'
response = urllib.request.urlopen(url)
lines = [l.decode('utf-8') for l in response.readlines()]
cr = csv.reader(lines)

for row in cr:
    #for i in range(len(row)):
        print(row)
