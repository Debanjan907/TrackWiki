import requests
import pandas as pd
import seaborn as sns
import datetime
import time

def get_url():
    host = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents"
    keyword = "Influenza"
    freq = "daily"
    start_date = "2014100100"
    end_date = "2015103100"
    url = "/".join([host, keyword, freq, start_date, end_date])
    print url
    return url

def clean_ts(ts):
    ts = ts.strip("00")
    yy = ts[0:4]
    mm = ts[4:6]
    dd = ts[6:8]
    date ="/".join([mm,dd,yy])
    ts = time.mktime(datetime.datetime.strptime(date, "%m/%d/%Y").timetuple())
    return ts

def parse_json(json_str):
    data = json_str
    df = pd.DataFrame(columns=['date','count'])
    for node in data["items"]:
        count = node["views"]
        ts = clean_ts(node["timestamp"])
        df = df.append({'date':ts,
                   'count':count
                   },ignore_index=True)
    print df
    return df

def fetch_data():
    url = get_url()
    r = requests.get(url)
    print "Status Code " + str(r.status_code)
    json_op = r.json();
    parse_json(json_op);

df = fetch_data()

sns.tsplot(df,time='date',value='count')