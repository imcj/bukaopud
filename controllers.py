#!-*- encoding: utf-8 -*-
import os
import web
import sys
import simplejson
import main

from pdb import set_trace as bp

github = {
  "before": "5aef35982fb2d34e9d9d4502f6ede1072793222d",
  "repository": {
    "url": "http://github.com/defunkt/github",
    "name": "github",
    "description": "You're lookin' at it.",
    "watchers": 5,
    "forks": 2,
    "private": 1,
    "owner": {
      "email": "chris@ozmm.org",
      "name": "defunkt"
    }
  },
  "commits": [
    {
      "id": "41a212ee83ca127e3c8cf465891ab7216a705f59",
      "url": "http://github.com/defunkt/github/commit/41a212ee83ca127e3c8cf465891ab7216a705f59",
      "author": {
        "email": "chris@ozmm.org",
        "name": "Chris Wanstrath"
      },
      "message": "okay i give in",
      "timestamp": "2008-02-15T14:57:17-08:00",
      "added": ["filepath.rb"]
    },
    {
      "id": "de8251ff97ee194a289832576287d6f8ad74e3d0",
      "url": "http://github.com/defunkt/github/commit/de8251ff97ee194a289832576287d6f8ad74e3d0",
      "author": {
        "email": "chris@ozmm.org",
        "name": "Chris Wanstrath"
      },
      "message": "update pricing a tad",
      "timestamp": "2008-02-15T14:36:34-08:00"
    }
  ],
  "after": "de8251ff97ee194a289832576287d6f8ad74e3d0",
  "ref": "refs/heads/master"
}

class DoIt:
	def __init__ ( self ):
		pass

class GitHub:
	def POST ( self ):
		raw_payload = web.input ( payload = "{}" ).payload.encode ( "utf-8" )
		pid = os.fork ( )
		if 0 == pid:
			main.deploy ( "dev", main.setting )
			sys.exit ( )
		fd = open ( "test.txt", "w+" )
		fd.write ( raw_payload )
		fd.close ( )
		payload = simplejson.loads ( raw_payload )
		if payload.has_key ( "ref" ):
			refs = payload['ref']

		# pid = os.fork ( )
		# if 0 == pid:
		# 	main.mail ( raw_payload )
		# 	sys.exit ( )
		return ""