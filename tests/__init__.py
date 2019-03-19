# -*- coding: utf-8 -*-

#    unwiki - remove wiki tags from a document
#    Copyright (C) 2016 Neil Freeman

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.#

import unittest
import unwiki


class unwikiTestCase(unittest.TestCase):

    def testLink(self):
        self.assertEqual(unwiki.loads('etc [[relative|link]] foo'), 'etc link foo')
        assert unwiki.loads('[[link]]') == 'link'
        self.assertEqual(unwiki.loads('[[relative link|link]]'), 'link')
        self.assertEqual(unwiki.loads('etc [[relative-link|link]] foo'), 'etc link foo')
        assert unwiki.loads('[[link (subject)|link]]') == 'link'

        assert unwiki.loads('[[Bar, Foo|Baz]], [[Foo]]') == 'Baz, Foo'

    def testComment(self):
        assert unwiki.loads('<!-- comment -->foo') == 'foo'

    def testHeadline(self):
        self.assertEqual(unwiki.loads('=== Head ==='), ' Head ')
        self.assertEqual(unwiki.loads('=== Head ===\nText'), ' Head \nText')

    def testCompressSpaces(self):
        self.assertEqual(unwiki.loads('removing this {{thing}} leaves extra spaces', True), 'removing this leaves extra spaces')

    def testInfobox(self):
        self.assertEqual(unwiki.loads('{{Infobox none}} None'), ' None')
        self.assertEqual(unwiki.loads('{{foo bar}}'), '')
        self.assertEqual(unwiki.loads("""{{foo\nbar}}"""), '')

        self.assertEqual(unwiki.loads("""{{Infobox
            foo}} None"""), ' None')

    def testRE(self):
        assert unwiki.RE.sub('x', '[[foo]]') == 'xfoox'
        assert unwiki.RE.sub('x', '{{foo}}') == 'x'
        assert unwiki.RE.sub('x', '{{foo\nbar}}') == 'x'

    def testList(self):
        lis = '* foo\n * bar\n ** [[baz]]'
        self.assertEqual(unwiki.loads(lis), "* foo\n * bar\n ** baz")

    def testFreeform(self):

        infobox = '''{{Infobox settlement
        <!--See Template:Infobox settlement for additional fields that may be available-->
        <!--See the Table at Infobox settlement for all fields and descriptions of usage-->
        <!-- General information  --------------->
        |timezone               = [[Eastern Time Zone|Eastern Standard Time]]
        |utc_offset             = -5
        }}'''

        self.assertEqual(unwiki.loads(infobox), '')

        markup = """{{about|the borough in New York City}}\n'''Staten Island ''' {{IPAc-en|ˌ|s|t|æ|t|ən|_|ˈ|aɪ|l|ə|n|d}} is one of the five [[borough (New York City)|boroughs]] of [[New York City]], in the U.S. state of [[New York]]."""
        expect = "\nStaten Island   is one of the five boroughs of New York City, in the U.S. state of New York."

        self.assertEqual(unwiki.loads(markup), expect)

        markup = """In the southwest of the city, Staten Island is the southernmost part of both the city and state of New York, with [[Conference House Park]] at the southern tip of the island and the state.<ref>{{cite web|website=http://www.nycgovparks.org/parks/conferencehousepark|title=Conference House Park|publisher=New York City Parks|accessdate=June 21, 2014}}</ref>"""
        expect = """In the southwest of the city, Staten Island is the southernmost part of both the city and state of New York, with Conference House Park at the southern tip of the island and the state."""
        self.assertEqual(unwiki.loads(markup), expect)

    def testMath(self):
        markup1 = "the field {{math|'''R'''}} of real numbers"
        expect1 = "the field _inline_math_ of real numbers"
        self.assertEqual(unwiki.loads(markup1), expect1)
        markup2 = "the field {{  math |'''R'''}} of real numbers"
        expect2 = "the field _inline_math_ of real numbers"
        self.assertEqual(unwiki.loads(markup2), expect2)
        # Check the same for the mvar teplate
        markup1 = "the field {{mvar|'''R'''}} of real numbers"
        expect1 = "the field _inline_math_ of real numbers"
        self.assertEqual(unwiki.loads(markup1), expect1)
        markup2 = "the field {{  mvar |'''R'''}} of real numbers"
        expect2 = "the field _inline_math_ of real numbers"
        self.assertEqual(unwiki.loads(markup2), expect2)

        # math tags
        markup3 = "with a [[norm (mathematics)|norm]] <math>\|\cdot\|_X</math>"
        expect3 = "with a norm _inline_math_"
        self.assertEqual(unwiki.loads(markup3), expect3)

    def testBracketFilenames(self):
        markup = """[[image:050712_perm_3.png|thumb|upright=1.7|Diagram of a cyclic permutation with two fixed points; a 6-cycle and two 1-cycles. |190x190px]]
A [[permutation]] is called"""
        expect = "\nA permutation is called"
        self.assertEqual(unwiki.loads(markup), expect)

    def testHTMLspaces(self):
        markup1 = "Let  &nbsp;''X''&nbsp;  be a non-negative integer and &nbsp;''n''&nbsp;"
        expect1 = "Let   X   be a non-negative integer and  n "
        self.assertEqual(unwiki.loads(markup1), expect1)
        markup2 = "this should be a &lt;; and a &gt;"
        expect2 = "this should be a <; and a >"
        self.assertEqual(unwiki.loads(markup2), expect2)

    def testRefRemoval(self):
        markup1 = 'the best of a nation.<ref name="AdvisoryCommittee" />  In this way'
        expect1 = "the best of a nation.  In this way"
        self.assertEqual(unwiki.loads(markup1), expect1)
        markup2 = """[[Jacques Le Goff]]<ref name="Le Goff">Le Goff, Jacques. ''La civilisation de l'Occident médieval''. Paris. 1964; English translation (1988): ''Medieval Civilization'', {{ISBN|0-631-17566-0}} &ndash; "translatio imperii" is discussed in Part II, Chapter VI, section on "Time, eternity and history".</ref> describes"""
        expect2 = """Jacques Le Goff describes"""
        self.assertEqual(unwiki.loads(markup2), expect2)

    def testBlockRemoval(self):
        markup1 = "this is a \n<blockquote>\n macizo\nhello\n</blockquote>"
        expect1 = "this is a \n\n macizo\nhello\n"
        self.assertEqual(unwiki.loads(markup1), expect1)

    def testNestedFileBracketRemoval(self):
        markup1 = """[[File:LA-Triceratops mount-2.jpg|thumb|250px|left|''[[Triceratops]]'' skeleton, [[Natural History Museum of Los Angeles County]]]]
Under [[phylogenetic nomenclature]], dinosaurs"""
        expect1 = """\nUnder phylogenetic nomenclature, dinosaurs""" 
        self.assertEqual(unwiki.loads(markup1), expect1)

    def testNestedCurlyBracketRemoval(self):
        markup1 = ''' Trying out {{the removal {{nested curly brackets}}}}'''
        expect1 = ' Trying out '
        markup2 = ''' Trying out {{the removal {{nested curly brackets}} this is looking pretty good }}'''
        expect2 = ' Trying out '
        markup3 = ''' Trying out If {{nowrap|log\u2009\'\'f\'\'(\'\'x\'\'; \'\'θ\'\')}} is {{nowrap| log θ the removal }}'''
        expect3 = ' Trying out If  is '
        self.assertEqual(unwiki.loads(markup1), expect1)
        self.assertEqual(unwiki.loads(markup2), expect2)
        self.assertEqual(unwiki.loads(markup3), expect3)

    def testREFTagIsConsumedCorrectly(self):
        markup1 = "hi <ref I should not see this/> And I should see this <ref> this not</ref>"
        expect1 = "hi  And I should see this "
        markup2 = "Now <ref>Remove This</ref> and forget <ref about this/>"
        expect2 = "Now  and forget "
        self.assertEqual(unwiki.loads(markup1), expect1)
        self.assertEqual(unwiki.loads(markup2), expect2)





if __name__ == '__main__':
    unittest.main()
