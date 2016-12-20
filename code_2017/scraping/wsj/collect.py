import requests as r
from utility import u_and_p, log, make_request
import datetime as dt
from datetime import datetime, timedelta
from json import dumps

from dateutil.parser import parse
from bs4 import BeautifulSoup


import sqlite3

#http://www.wsj.com/search/term.html?min-date=2012/12/19&max-date=2016/12/19&page=2501&isAdvanced=true&daysback=4y&andor=AND&sort=date-desc&source=wsjarticle,wsjblogs,sitesearch


def generate_page_links(self, min_date, max_date):

	"""
	WARNING THIS IS AN INFINITE GENERATOR YOU MUST EXPLICITLY CALL BREAK

	"""

	yield "http://www.wsj.com/search/term.html?min-date={min_date}&max-date={max_date}&isAdvanced=true&daysback=4y&andor=AND&sort=date-desc&source=wsjarticle,wsjblogs,sitesearch".format(
		min_date = min_date,
		max_date = max_date)

	page_number  = 0

	while True:
		yield "http://www.wsj.com/search/term.html?min-date={min_date}&max-date={max_date}&page={page}&isAdvanced=true&daysback=4y&andor=AND&sort=date-desc&source=wsjarticle,wsjblogs,sitesearch".format(
			min_date = min_date,
			max_date = max_date,
			page = page_number,
		)

		page_number += 1

def parse_page(self, html):

	if "No articles or videos have been found." in html:
		return []

	bs_obj = BeautifulSoup(html, 'lxml')

	results = bs_obj.select_one("body > div.pageFrame > div.contentFrame.wsj-sectionfront.sf-automated-news > section.sector.two > div.col12.column.one.search-body > div.search-results-sector > div.zonedModule > div.module.automated-news.search-results")

	if not results:

		raise Exception('Search results not found in body or strucutre of page is different')

	articles = result.select('ul.items.hedSumm > li > div.item-container.headline-item')


	def _parse_article(article):
		pass


	return [_parse_article(x) for x in articles]






class Links:

    def __init__(self):

        self.db = sqlite3.connect('wsj.db')  

        self.cursor = self.db.cursor()
        self.REQUEST_TIMEOUT = 1
        self.ERROR_TIMEOUT = 1800
        self.session = None

    def _create(self):

        """
        create

        Creates the Links Processed and Links Tables.

        """

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ARTICLES(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            BEGIN_DATE DATE,
            END_DATE DATE,
            WEB_URL TEXT,
            CATEGORY TEXT,
            AUTHOR TEXT,
            PUB_DATE DATE,
            HTML TEXT)""")

        self.db.commit()

    def _insert_articles(self, obj):

        """
        insert_into_table

        Inserts a tuple into the links table.

        """

        self.cursor.execute("""
            INSERT INTO ARTICLES(
            BEGIN_DATE,
            END_DATE,
            WEB_URL,
            CREATED,
            SECTION_NAME,
            KEYWORDS,
            NYTDDES,
            NEWS_DESK,
            PUB_DATE,
            SUBSECTION_NAME,
            TAXONOMY_NODES,
            TIMESMACHINE_URL,
            ASSET_ID,
            MULTIMEDIA,
            HEADLINE,
            TYPE_OF_MATERIAL,
            PAY,
            ABSTRACT,
            SNIPPET,
            SOURCE,
            ARTICLE_ID,
            UPDATED,
            DOCUMENT_TYPE,
            LEAD_PARAGRAPH,
            BYLINE,
            HTML) VALUES (?,  ?,  ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,? , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)""", obj)

        self.db.commit()

    def _form_url(self, begin, end):

        """

        _form_url

        begin : String -> end : String -> Result: String

        Generator that yields the url name for the archive api.
        Does not check if response if empty that has to be done manually.

        """

        begin_formatted, end_formatted =  self._format_date_obj(begin), self._format_date_obj(end)

        yield 'http://query.nytimes.com/svc/add/v1/sitesearch.json?end_date={end}&begin_date={begin}&facet=true'.format(
            begin = begin_formatted, 
            end = end_formatted)

        for i in range(1,101):
                yield 'http://query.nytimes.com/svc/add/v1/sitesearch.json?end_date={end}&begin_date={begin}&page={page}&facet=true'.format(
                    begin = begin_formatted, 
                    end = end_formatted,
                    page = i)


    def _get_article(self, url):

        """
        _get_article

        url: String ->  Return : String

        Given a article url returns the html of that article

        """

        return make_request(
            url,
            {},
            self.REQUEST_TIMEOUT,
            self.ERROR_TIMEOUT,
            session = self.session, 
            return_json = False,
            refresh_session = None)


    def _parse_response(self, response):

        """

        _parse_response

        Json Obj -> (List<Large Fucking Tuple> | None)

        Takes a response object and prepares it to be written in sql table.


        """

        body = response.get('response').get('docs') 

        def _parse(item):

            """

            _parse

            Given a json archives response returns all relenvant values as well as the html of the article

            """

            simple_categories = ('snippet', 'abstract', 'lead_paragraph', 'type_of_material', 'pub_date',
                'created', 'updated', 'source', 'print_section', 'web_url', 'taxonomy_nodes',
                'byline', 'pay', 'document_type', 'asset_id', '_id','timesmachine_url')

            (snippet, abstract, lead_paragraph, type_of_material, pub_date, created, updated, source,
                print_section, web_url, taxonomy_nodes, byline, pay, document_type, asset_id, _id, timesmachine_url
                ) = [item.get(name) for name in simple_categories]

            # Lol too lazy to make actual tables for this stuff
            # maybe should have went nosql. rekt()
            # to reader:
            # Thesse fields correspond to lists of dicationaries
            # I just encoded them as strings and saved the strings

            json_categories = ('headline', 'section_name', 'subsection_name', 'keyword', 'multimedia', 'news_desk', 'nytddes')

            headline, section_name, subsection_name, keywords, multimedia, news_desk, nytddes = [dumps(item.get(x)) for x in json_categories]

            html = self._get_article(web_url)
            # THIS ORDER MATTERS 

            return (web_url, created, section_name, keywords, nytddes, news_desk, pub_date, subsection_name, taxonomy_nodes, timesmachine_url, asset_id,
                multimedia, headline, type_of_material, pay, abstract, snippet, source, _id, updated, document_type, lead_paragraph, byline, html)

        if not body:
            return None

        return [_parse(x) for x in body]


    def _get_latest_date(self):

        """

        _get_latest_date

        -> Date Object

        Reads the database for the most recent entry into into the links table.
        Uses that entry to construct a date time object. If the table is empty
        simply takes today's date.

        """

        max_id = self.cursor.execute('SELECT MAX(ID) FROM ARTICLES').fetchone()[0]

        if not max_id:

            return dt.datetime.today()




        latest_date = self.cursor.execute("""SELECT BEGIN_DATE FROM ARTICLES WHERE id = {}""".format(max_id)).fetchone()[0]

        return parse(latest_date)



    def _format_date_obj(self, date_obj):

        """

        _format_date_obj

        date_obj : Date -> String

        Returns a date that can be fed to nytimes api


        """

        return date_obj.isoformat().split('T')[0].replace("-", '')

    def _get_json(self, url):

        """

        _get_json

        Give a url of archives api. I will give you back the json of it.


        """

        return make_request(
            url,
            {},
            self.REQUEST_TIMEOUT,
            self.ERROR_TIMEOUT,
            session = self.session,
            return_json = True,
            refresh_session = None)


    def get_link(self):

        """
        get_link

        -> 

        This functions adds articles to articles table.

        """

        self._create()

        most_recent_date = self._get_latest_date()

        date = most_recent_date

        two_days_ago = date - timedelta(days=2)

        for i in range(10):

            log('Processing date {}'.format(date))

            i = 0

            for url in self._form_url(end = date, begin = two_days_ago):

                if i == 2:
                    continue
                i +=1

                res  = self._get_json(url)

                parsed_responses = self._parse_response(res)

                if not parsed_responses:
                    continue

                for article in parsed_responses:

                    row = (two_days_ago, date) +  article
                    self._insert_articles(row)
                    log("Row added to articles table")


            date = two_days_ago

            two_days_ago = two_days_ago - timedelta(days=2)


if __name__ == "__main__":
    r = Links()

