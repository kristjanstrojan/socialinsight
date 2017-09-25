import requests
import xml.etree.ElementTree as ET

class RSS():

    def __init__(self, url):
        self.url = url
        self.result = []


    def __iter__(self):
        self._parse()
        return iter(self.result)


    def _parse(self):
        for url in self.url:
            rss = requests.get(url)
            get_text = unicode(rss.text)
            text = get_text.encode("utf-8")

            root = ET.fromstring(text)

            channel = root.find("channel")

            for row in channel.findall("item"):
                print(row)
                self.result.append(dict(
                    text=row.find("title").text,
                    channel='rss::'+str(url),
                    url = row.find('link').text,
                    date = row.find('pubDate').text
                )
            )

    def get(self):
        self._parse()
        return self.result
