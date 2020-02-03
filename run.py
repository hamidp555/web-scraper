from ruamel import yaml
import redis
import logging
import json

logger = logging.getLogger('settings')


class Settings(object):
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            crawl_config = yaml.load(f, Loader=yaml.Loader)
            self.endpoint = crawl_config.get('schedule_crawl_endpoint')
            self.project_name = crawl_config.get('project_name')
            self.project_version = crawl_config.get('project_version')
            self.spiders = crawl_config.get('spiders')
            self.reids_host = crawl_config.get('reids_host')
            self.redis_port = crawl_config.get('redis_port')
            self.redis_password = crawl_config.get('redis_password')


def main():
    settings = Settings('crawl_config.yaml')
    r = redis.Redis(
        host=settings.reids_host,
        port=settings.redis_port,
        password=settings.redis_password
    )

    for spider in settings.spiders:
        spider_name = spider.get('name')
        logger.debug('adding start_urls for {} spider'.format(spider_name))
        key = '{}:start_urls'.format(spider_name)

        for start_url in spider.get('start_urls'):
            logger.debug('{} added to redis'.format(start_url))
            r.lpush(key, start_url)

        # for distributed replying on worker queues
        worker_queue_item = json.dumps(
            {'project': settings.project_name, 'spider': spider_name})
        r.lpush('workers:spiders', worker_queue_item)


if __name__ == "__main__":
    main()
