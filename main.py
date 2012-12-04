#!/usr/bin/env python
#! -*- encoding: utf-8 -*-

import os
import sys
import time
import subprocess
import smtplib

from StringIO import StringIO
from pdb import set_trace as bp

ROOT = os.path.dirname ( os.path.join ( os.getcwd ( ), __file__ ) )
REPOSITORY_DIR = os.path.join ( ROOT, "repos" )

if not os.path.isdir ( REPOSITORY_DIR ):
	os.makedirs ( REPOSITORY_DIR )

setting = {
	'ap_email'    : os.getenv ( "AP_EMAIL" ),
	'ap_passwd'   : os.getenv ( "AP_PASSWD" ),
	'ap_app'      : os.getenv ( "AP_APP" ),
	'smtp_host'   : os.getenv ( "SMTP_HOST" ),
	'smtp_user'   : os.getenv ( "SMTP_USER" ),
	'smtp_passwd' : os.getenv ( "SMTP_PASSWD" ),
	'application_root' : ROOT,
}

class CMDResult:
	def __init__ ( self, cmd, out = "", err = "", start_time = 0, end_time = 0 ):
		self.cmd = cmd
		self.out = out
		self.err = err
		self.start_time = start_time
		self.end_time = end_time

	def execute_time ( self ):
		return self.end_time - self.start_time

	def __str__ ( self ):
		return "[%s [%ds]]\n%s%s" % ( self.cmd, self.execute_time ( ), self.out, self.err )

class CMD:
	cmds = []
	fd_out = []
	fd_err = []

	def __init__ ( self ):
		pass

	def open ( self, cmd ):
		result = CMDResult ( cmd )
		result.start_time = time.time ( )
		self.cmds.append ( result )
		pin_fd, pout_fd, perr_fd = os.popen3 ( cmd  )
		out = pout_fd.read ( )
		err = perr_fd.read ( )

		result.out = out
		result.err = err

		self.fd_out.append ( out )
		self.fd_err.append ( err )

		result.end_time = time.time ( )

		return result

	def allDescription ( self ):
		buf = StringIO ( )
		for i in range ( len ( self.cmds ) ):
			result = self.cmds[i]
			buf.write ( str ( result ) )
			buf.seek ( 0 )

		return buf.read ( )

def deploy ( branch, setting ):

	repos_path = os.path.join ( REPOSITORY_DIR, "post_bar" )

	clone = False
	# bp ()
	if not os.path.exists ( repos_path ):
		os.chdir ( REPOSITORY_DIR )
		pin_fd, pout_fd, perr_fd = os.popen3 ( "git clone http://github.com/shitou/post_bar"  )
		clone = True
		
	os.chdir ( repos_path )
	
	cmd = CMD ( )
	if not clone:
		cmd.open ( "git checkout %s" % ( branch ) )
		cmd.open ( "git pull"  )
		cmd.open ( "%(application_root)s/af/bin/af login %(ap_email)s --passwd %(ap_passwd)s" % setting  )
		cmd.open ( "%(application_root)s/af/bin/af update %(ap_app)s" % setting  )
		cmd.open ( "%(application_root)s/af/bin/af logs %(ap_app)s" % setting  )

	mail ( cmd.allDescription ( ) )

def mail ( content ):
	client = smtplib.SMTP_SSL ( setting['smtp_host'] )
	client.login ( setting['smtp_user'], setting['smtp_passwd'] )
	client.sendmail ( "weicongju@gmail.com", [ "weicongju@gmail.com" ], content )
	client.quit ( )

if "__main__" == __name__:
	deploy ( "dev", setting )