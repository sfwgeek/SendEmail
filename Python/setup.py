#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: et sw=4 ts=4:
"""
DESCRIPTION:
    Used by py2exe to make binaries.
AUTHOR:
    sfw geek
"""

from distutils.core import setup
import py2exe


class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)

        self.version = '0.0.1'
        self.company_name = 'sfwgeek'
        self.copyright = 'Copyright © sfwgeek 2014'
        self.name = 'SendEmail'

target = Target(
    description = 'Command Line Interface (CLI) program to send email.',
    script = 'SendEmail.py',
    dest_base = 'SendEmail')

setup(
    options = {
        'py2exe': {
            'compressed': 1,
            'dll_excludes': [ 'w9xpopen.exe' ],
            'optimize': 2,
            #'ascii': 1,
            'bundle_files': 1
        }
    },
    zipfile = None,
    console = [target]
)
