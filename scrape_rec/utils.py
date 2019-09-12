import os
import gzip

import pickle
from scrapy.http import Headers
from scrapy.responsetypes import responsetypes
from w3lib.http import headers_raw_to_dict


def get_metadata(rpath):
    with open(os.path.join(rpath, 'pickled_meta'), 'rb') as f: 
        return pickle.load(f) 


def get_gzip_metadata(rpath):
    with gzip.open(os.path.join(rpath, 'pickled_meta'), 'rb') as f: 
        return pickle.load(f)


def get_response_from_cache_by_id(rpath):
    metadata = get_metadata(rpath)

    with open(os.path.join(rpath, 'response_body'), 'rb') as f: 
        body = f.read() 
     
    with open(os.path.join(rpath, 'response_headers'), 'rb') as f: 
        rawheaders = f.read() 
 
    url = metadata.get('response_url') 
    status = metadata['status'] 
    headers = Headers(headers_raw_to_dict(rawheaders)) 
    respcls = responsetypes.from_args(headers=headers, url=url) 
    response = respcls(url=url, headers=headers, status=status, body=body) 
 
    return response 


HTTPCACHE_DIR = '/var/lib/httpcache/'


def get_all_responses_from_cache(spider):
    root_dir = os.path.join(HTTPCACHE_DIR, spider.name)
    for current_root, directories, files in os.walk(root_dir): 
        if files and not directories: 
            yield get_response_from_cache_by_id(current_root) 


def get_all_urls_from_httpcache(spider_name):
    root_dir = os.path.join(HTTPCACHE_DIR, spider_name)
    for current_root, directories, files in os.walk(root_dir): 
        if files and not directories: 
            try:
                meta = get_metadata(current_root)
            # Metadata may be encoded using gzip
            except:
                meta = get_gzip_metadata(current_root)
            yield meta.get('url')
