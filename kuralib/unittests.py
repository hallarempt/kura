#!/usr/bin/env python
"""
  Unittests for the kuralib middleware
"""

import unittest, sys, string, codecs, time

import kuraapp

class KuraAppTestCase(unittest.TestCase):

    def testCreateRepository(self):
        kuraapp.initApp("boud", "andal", "", "localhost")
        app = kuraapp.app
        assert len(app.tables) > 0,  "Tables not filled."
        assert len(app.relations) > 0, "Relations not filled."
        assert len(app.objects) > 0, "Objects not defined."
        assert app.sql

def suite():
    s1 = unittest.makeSuite(KuraAppTestCase, "test")
    testSuite=unittest.TestSuite((s1,))
    return testSuite

def main():
    runner = unittest.TextTestRunner(sys.stderr, 1, 2)
    runner.run(suite())

if __name__=="__main__":
    main()


__copyright__="""
/***************************************************************************
        copyright                        : (C) 2002 by Boudewijn Rempt 
                                            see copyright notice for license
        email                            : boud@valdyas.org
        Revision                         : $Revision: 1.6 $
        Last edited                      : $Date: 2002/11/16 13:43:59 $
        
 ***************************************************************************/
"""
