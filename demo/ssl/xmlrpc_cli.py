#!/usr/bin/env python

"""Demonstration of M2Crypto.xmlrpclib2.

Copyright (c) 1999-2003 Ng Pheng Siong. All rights reserved."""

RCS_id='$Id: xmlrpc_cli.py,v 1.4 2002/12/23 04:43:31 ngps Exp $'

from M2Crypto import Rand
from M2Crypto.m2xmlrpclib import Server, SSL_Transport

def ZServerSSL():
    # Server is Zope-2.3.0 on ZServerSSL.
    zs = Server('https://127.0.0.1:9443/', SSL_Transport())
    print zs.propertyMap()

def xmlrpc_srv():
    # Server is ../https/START_xmlrpc.py or ./xmlrpc_srv.py.
    zs = Server('https://127.0.0.1:9443', SSL_Transport())
    print zs.Testing(1, 2, 3)
    print zs.BringOn('SOAP')

if __name__ == '__main__':
    Rand.load_file('../randpool.dat', -1)
    #ZserverSSL()
    xmlrpc_srv()
    Rand.save_file('../randpool.dat')

