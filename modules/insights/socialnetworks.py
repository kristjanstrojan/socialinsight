import tweepy
import json
import datetime
import time
import requests

from . import secrets 

date_end = datetime.datetime.now()
end = date_end.strftime('%Y-%m-%d')
date_start = date_end - datetime.timedelta(days=7)
start = date_start.strftime('%Y-%m-%d')


class SocialNetworks:

    def __init__(self, accounts):
        self.accounts=accounts
        self.result = []

    def __iter__(self):
        self.twitter()
        self.facebook()
        return iter(self.result)

    def twitter(self):
        """
        This is method for searching tweets from specific user.
        """
        access_token = secrets.twitter_access_token
        access_token_secret = secrets.twitter_access_token_secret
        consumer_key = secrets.twitter_consumer_key
        consumer_secret = secrets.twitter_consumer_secret

        # Twitter auth using 'tweepy' module.
        # Docs at: http://tweepy.readthedocs.io/
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        # Build search query for Twitter.
        from_q = list(map(lambda x: 'from:'+x, self.accounts))
        query = " OR ".join(from_q)
        search  = api.search(query)

        for s in search:
            try:
                url ="http://twitter.com/{user}/status/{id}".format(
                    user=s.user.id,
                    id=s.id
                )
                usrn = unicode(s.user.name)
                usr = usrn.encode('utf-8')
                self.result.append(dict(
                    text=s.text,
                    channel='tw::'+str(usr),
                    url = url,
                    date = s.created_at
                )
            )
            except:
                # Silently pass.
                pass


    def facebook(self):
        client_id = secrets.facebook_client_id
        client_secret = secrets.facebook_client_secret
        fb_base = "https://graph.facebook.com/v2.8"
        oauth_url = ("{fb_base}/oauth/access_token?"
                     "client_id={client_id}&"
                     "client_secret={client_secret}&"
                     "grant_type=client_credentials").format(
                         fb_base=fb_base,
                         client_id=client_id,
                         client_secret=client_secret
                     )
        r = requests.get(oauth_url)
        if r.status_code != requests.codes.ok:
            return dict(success=False, message='Something went wrong at Facebook request.')

        if 'access_token' not in r.json():
            return dict(success=False, message='Error obtaining access token from Facebook.')
        else:
            ac = r.json()['access_token']

        # get string from account list
        account_string = ",".join(self.accounts)

        for a in self.accounts:
            account_string = a
            stat_url = ("{fb_base}/posts?"
                        "ids={account_string}&"
                        "since={start}&"
                        "until=now&limit=100&"
                        "access_token={ac}").format(
                            fb_base=fb_base,
                            account_string=account_string,
                            start=start,
                            ac=ac)
            statuses = requests.get(stat_url)
            stat = statuses.json()
            try:
                for s in stat[a]['data']:
                    story = s['story'] if 'story' in s.keys() else ''
                    message = s['message'] if 'message' in s.keys() else ''
                    text = story + " " + message if story else message


                    p_url = requests.get(("{fb_base}/{s_id}?"
                                         "fields=permalink_url,created_time&"
                                         "access_token={ac}").format(
                                             fb_base=fb_base,
                                             s_id=s['id'],
                                             ac=ac))
                    url = p_url.json()['permalink_url']
                    date_string = p_url.json()['created_time']
                    date = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S+0000')

                    self.result.append(
                        dict(
                            text=text,
                            channel='fb::'+a,
                            url=url,
                            date=date
                        )
                    )
            except:
                # Fail silently
                pass
