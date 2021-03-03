import csv, urllib.request
import schedule


def job():

    url = 'http://ilmanet.fi/download.php?orderId=93173&id=127&type=solar&limit=1'
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cr = csv.reader(lines)

    with open('file4.csv', 'w') as f:
        for row in cr:
            for x in row:
                f.write(str(x) + ',')
            f.write('\n')
    return
schedule.every(1).minutes.do(job)
#schedule.every().hour.do(job)

while True:
    schedule.run_pending()


#for row in cr:
    #for i in range(len(row)):
        #print(row)


