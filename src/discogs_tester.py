#!/usr/bin/python

import discogs_client
import time


if __name__ == "__main__":
    discogs = DiscogsClient()
    result = discogs.search_for_release('659457206512')
    
    print result.title
