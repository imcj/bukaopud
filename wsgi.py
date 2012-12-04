#!/usr/bin/env python
#! -*- encoding: utf-8 -*- 

import web
import controllers

app = web.application ( ( '/github/', 'controllers.GitHub' ), globals ( ) )

application = app.wsgifunc ( )

if __name__ == "__main__":
   app.run ( )