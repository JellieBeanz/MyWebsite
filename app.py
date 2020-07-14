import os
import sys
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import matplotlib.pyplot as plt
import mpld3
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_recaptcha import ReCaptcha
from datetime import datetime

from twilio.rest import Client
from decouple import config

number = config('NUMBER')
accSID = config('TWILIO_ACCOUNT_SID')
auth = config('TWILIO_AUTH_TOKEN')

site_key = config('RECAPTCHA_PUBLIC_KEY')
secret_key = config('RECAPTCHA_PRIVATE_KEY')

client = Client(accSID, auth)

from_whatsapp_number = '+441753208643'
to_whatsapp_number = number


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

app.config.update({'RECAPTCHA_ENABLED': True,
                   'RECAPTCHA_SITE_KEY':
                       site_key,
                   'RECAPTCHA_SECRET_KEY':
                       secret_key})

recaptcha = ReCaptcha(app=app)

url = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,CHZ,LEND,UBT,FET,ETH,VET,CELR,THETA,LTC,MCO,BNB,EOS,XLM,MNE,XTZ,CRO,WAVES,ZIL,RVN,USDC,ENJ,LINK,NRG,BAT,USDT,ENJ,KICK,SNX,KNC,REN&tsyms=EUR,BTC'
parameters = {

}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '76d3c96e-8087-4895-877d-b73e88ed0efa',
}

session = Session()
session.headers.update(headers)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/')
def index():

    try:
        return render_template('index.html')
    except:
        return 'Could not delete task'


@app.route('/metals')
def render_metals():

    try:
        return render_template('metals.html')
    except:
        return 'Could not connect to metals.html - make sure you have an internet connection'


@app.route('/whatsapp', methods=['POST', 'GET'])
def sendmessage():

    if recaptcha.verify():
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        try:
            client.messages.create(body='From: ' + name + ' Email: ' + email + ' Message: ' + message,
                                from_=from_whatsapp_number,
                                to=to_whatsapp_number)
            return redirect('/')
        except:
            return 'Could not send message'
    else:
        return 'Recaptcha Error'


@app.route('/taskmaster', methods=['POST', 'GET'])
def taskmaster():

    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/taskmaster')
        except:
            return 'Error uploading task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('taskmaster.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/taskmaster')
    except:
        return 'Could not delete task'


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/taskmaster')
        except:
            return 'Could not update task'
    else:
        return render_template('update.html', task=task)


@app.route('/portfolio', methods=['POST', 'GET'])
def bitcoin():

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        myBTC = 1.00281086
        myETH = 2.0268
        myLINK = 256.47
        myEOS = 5.7428
        myXLM = 1
        myNRG = 27.5
        myBAT = 248.7737
        myUSDT = 0.83952
        myBNB = 0.02348929
        myCRO = 45.99
        myZIL = 9000
        myWAVES = 0
        myRVN = 0
        myMCO = 100
        myUSDC = 269.17
        myXTZ = 47.71207716
        myENJ = 1827.73543307
        mySNX = 207.76676515
        myKNC = 243.81136694
        myREN = 1577.07449686
        myKICK = 888888
        myMNE = 64000
        myVET = 7000
        myTHETA = 500
        myCELR = 6000
        myCHZ = 0
        myLEND = 914.82554757
        myUBT = 309.58876449
        myFET = 0

        btcEUR = data['BTC']['EUR']
        ethEUR = data['ETH']['EUR']
        linkEUR = data['LINK']['EUR']
        eosEUR = data['EOS']['EUR']
        xlmEUR = data['XLM']['EUR']
        nrgEUR = data['NRG']['EUR']
        batEUR = data['BAT']['EUR']
        usdtEUR = data['USDT']['EUR']
        bnbEUR = data['BNB']['EUR']
        croEUR = data['CRO']['EUR']
        usdcEUR = data['USDC']['EUR']
        zilEUR = data['ZIL']['EUR']
        enjEUR = data['ENJ']['EUR']
        mcoEUR = data['MCO']['EUR']
        wavesEUR = data['WAVES']['EUR']
        kickEUR = data['KICK']['EUR']
        snxEUR = data['SNX']['EUR']
        kncEUR = data['KNC']['EUR']
        renEUR = data['REN']['EUR']
        rvnEUR = data['RVN']['EUR']
        mneEUR = data['MNE']['EUR']
        xtzEUR = data['XTZ']['EUR']
        vetEUR = data['VET']['EUR']
        thetaEUR = data['THETA']['EUR']
        celrEUR = data['CELR']['EUR']
        chzEUR = data['CHZ']['EUR']
        lendEUR = data['LEND']['EUR']
        ubtEUR = data['UBT']['EUR']
        fetEUR = data['FET']['EUR']
        

        totalBTC_EUR = round(myBTC*btcEUR, 2)
        totalETH_EUR = round(myETH*ethEUR, 2)
        totalEOS_EUR = round(myEOS*eosEUR, 2)
        totalXLM_EUR = round(myXLM*xlmEUR, 2)
        totalLINK_EUR = round(myLINK*linkEUR, 2)
        totalMCO_EUR = round(myMCO*mcoEUR, 2)
        totalNRG_EUR = round(myNRG*nrgEUR, 2)
        totalBAT_EUR = round(myBAT*batEUR, 2)
        totalUSDT_EUR = round(myUSDT*usdtEUR, 2)
        totalBNB_EUR = round(myBNB*bnbEUR, 2)
        totalCRO_EUR = round(myCRO*croEUR, 2)
        totalUSDC_EUR = round(myUSDC*usdcEUR, 2)
        totalZIL_EUR = round(myZIL*zilEUR, 2)
        totalENJ_EUR = round(myENJ*enjEUR, 2)
        totalKICK_EUR = round(myKICK*kickEUR, 2)
        totalWAVES_EUR = round(myWAVES*wavesEUR, 2)
        totalSNX_EUR = round(mySNX*snxEUR, 2)
        totalKNC_EUR = round(myKNC*kncEUR, 2)
        totalREN_EUR = round(myREN*renEUR, 2)
        totalRVN_EUR = round(myRVN*rvnEUR, 2)
        totalMNE_EUR = round(myMNE*mneEUR, 2)
        totalXTZ_EUR = round(myXTZ*xtzEUR, 2)
        totalVET_EUR = round(myVET*vetEUR, 2)
        totalTHETA_EUR = round(myTHETA*thetaEUR, 2)
        totalCELR_EUR = round(myCELR*celrEUR, 2)
        totalCHZ_EUR = round(myCHZ*chzEUR, 2)
        totalLEND_EUR = round(myLEND*lendEUR, 2)
        totalUBT_EUR = round(myUBT*ubtEUR, 2)
        totalFET_EUR = round(myFET*fetEUR, 2)
        
    

        total = totalLEND_EUR + totalUBT_EUR + totalFET_EUR + totalCHZ_EUR + totalCELR_EUR + totalVET_EUR + totalTHETA_EUR + totalBTC_EUR + totalMCO_EUR + totalETH_EUR + totalEOS_EUR + totalXLM_EUR + totalLINK_EUR + totalNRG_EUR + totalBAT_EUR + \
            totalUSDT_EUR + totalBNB_EUR + totalCRO_EUR + totalUSDC_EUR + totalZIL_EUR + totalENJ_EUR + \
            totalWAVES_EUR + totalSNX_EUR + totalKNC_EUR + \
            totalREN_EUR + totalRVN_EUR + totalXTZ_EUR

        totalOther = totalLEND_EUR + totalUBT_EUR + totalFET_EUR + totalCHZ_EUR + totalCELR_EUR + totalVET_EUR + totalTHETA_EUR + totalMCO_EUR + totalEOS_EUR + totalXLM_EUR + totalNRG_EUR + totalBAT_EUR + \
            totalUSDT_EUR + totalBNB_EUR + totalCRO_EUR + totalUSDC_EUR + totalZIL_EUR + \
            totalWAVES_EUR + totalSNX_EUR + totalKNC_EUR + \
            totalREN_EUR + totalRVN_EUR + totalXTZ_EUR

        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = 'Btc', 'Link', 'Snx', 'Eth', 'Other'
        sizes = [totalBTC_EUR, totalLINK_EUR,
                 totalSNX_EUR, totalETH_EUR, totalOther]
        # only "explode" the 2nd slice (i.e. 'Hogs')
        explode = (0.1, 0.1, 0.1, 0.1, 0.1)

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.axis('equal')

        plt.savefig('static/images/piechart.svg')
        return render_template('portfolio.html',
                               data=data, btcEUR=btcEUR, myBTC=myBTC, totalBTC_EUR=totalBTC_EUR,
                               ethEUR=ethEUR, myEth=myETH, totalETH_EUR=totalETH_EUR,
                               linkEUR=linkEUR, myLINK=myLINK, totalLINK_EUR=totalLINK_EUR,
                               croEUR=croEUR, myCRO=myCRO, totalCRO_EUR=totalCRO_EUR,
                               enjEUR=enjEUR, myENJ=myENJ, totalENJ_EUR=totalENJ_EUR,
                               usdcEUR=usdcEUR, myUSDC=myUSDC, totalUSDC_EUR=totalUSDC_EUR,
                               kncEUR=kncEUR, myKNC=myKNC, totalKNC_EUR=totalKNC_EUR,
                               zilEUR=zilEUR, myZIL=myZIL, totalZIL_EUR=totalZIL_EUR,
                               wavesEUR=wavesEUR, myWAVES=myWAVES, totalWAVES_EUR=totalWAVES_EUR,
                               rvnEUR=rvnEUR, myRVN=myRVN, totalRVN_EUR=totalRVN_EUR,
                               snxEUR=snxEUR, mySNX=mySNX, totalSNX_EUR=totalSNX_EUR,
                               renEUR=renEUR, myREN=myREN, totalREN_EUR=totalREN_EUR,
                               batEUR=batEUR, myBAT=myBAT, totalBAT_EUR=totalBAT_EUR,
                               mneEUR=mneEUR, myMNE=myMNE, totalMNE_EUR=totalMNE_EUR,
                               xtzEUR=xtzEUR, myXTZ=myXTZ, totalXTZ_EUR=totalXTZ_EUR,
                               eosEUR=eosEUR, myEOS=myEOS, totalEOS_EUR=totalEOS_EUR,
                               xlmEUR=xlmEUR, myXLM=myXLM, totalXLM_EUR=totalXLM_EUR,
                               nrgEUR=nrgEUR, myNRG=myNRG, totalNRG_EUR=totalNRG_EUR,
                               usdtEUR=usdtEUR, myUSDT=myUSDT, totalUSDT_EUR=totalUSDT_EUR,
                               bnbEUR=bnbEUR, myBNB=myBNB, totalBNB_EUR=totalBNB_EUR,
                               kickEUR=kickEUR, myKICK=myKICK, totalKICK_EUR=totalKICK_EUR,
                               mcoEUR=mcoEUR, myMCO=myMCO, totalMCO_EUR=totalMCO_EUR,
                               vetEUR=vetEUR, myVET=myVET, totalVET_EUR=totalVET_EUR,
                               thetaEUR=thetaEUR, myTHETA=myTHETA, totalTHETA_EUR=totalTHETA_EUR,
                               celrEUR=celrEUR, myCELR=myCELR, totalCELR_EUR=totalCELR_EUR,
                               chzEUR=chzEUR, myCHZ=myCHZ, totalCHZ_EUR=totalCHZ_EUR,
                               lendEUR=lendEUR, myLEND=myLEND, totalLEND_EUR=totalLEND_EUR,
                               fetEUR=fetEUR, myFET=myFET, totalFET_EUR=totalFET_EUR,
                               ubtEUR=ubtEUR, myUBT=myUBT, totalUBT_EUR=totalUBT_EUR,
                               total=round(total, 2)
                               )

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


if __name__ == "__main__":
    app.run(debug=True)
