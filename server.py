#!/usr/bin/env python
# encoding:utf-8
import os
import json
from flask import Flask, render_template, redirect, url_for
import requests
import ConfigParser
config = ConfigParser.SafeConfigParser()
config.read("config.ini")


app = Flask(__name__, static_folder = './static')
app.debug = True


with open('fake.json', 'r') as f:
  fake = json.load(f)


def trigger_maker(secretKey, event, values):
  url = "https://maker.ifttt.com/trigger/" + event + "/with/key/" + secretKey
  payload = {
    'value1': values[0],
    'value2': values[1],
    'value3': values[2]}
  headers = {'Content-Type': 'application/json'}
  r = requests.post(url, data=json.dumps(payload), headers=headers)
  return r.status_code

@app.route('/')
def index():
  return render_template('index.html',
    powered_by=os.environ.get('POWERED_BY', 'Hidenobu Hashikami'))

@app.route('/test')
def test():
  secretKey = config.get('maker', 'secret_key')
  event  = config.get('maker', 'event')
  value1 = config.get('maker', 'value1')
  value2 = config.get('maker', 'value2')
  value3 = config.get('maker', 'value3')
  trigger_maker(secretKey, event, [value1, value2, value3])
  return redirect(url_for('alert'))

@app.route('/alert')
def alert():
  medicines = fake['medicines']
  recautions = fake['recautions']
  return render_template('alert.html',
    medicines=medicines, recautions=recautions)

@app.route('/pharmacy')
def pharmacy():
  pharmacy = fake['pharmacy']
  return render_template('pharmacy.html',
    pharmacy=pharmacy)

@app.route('/record')
def record():
  return render_template('record.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
  # app.run(port=int(os.environ.get('PORT', 5000)))