from datetime import datetime


class TidyUp(object):
    def process_item(self, item, spider):
        item['scrape_date'] = datetime.now().isoformat()
        item['spider'] = spider.settings.get('BOT_NAME')
        item['project'] = spider.name
        return item
