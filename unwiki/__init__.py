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

import re
import html
from functools import reduce

def paren_matcher (n):
    # poor man's matched paren scanning, gives up
    # after n+1 levels.  Matches any string with balanced
    # parens inside; add the outer parens yourself if needed.
    # Nongreedy.
    return r"[^()]*?(?:\[\["*n+r"[^()]*?"+r"\]\][^()]*?)*?"*n

PRE = re.compile(r"""(?P<math>{{\s*(?:math|mvar)\s*\|)(.*?)(?(math)}}|)
                  """, re.X)

RE = re.compile(r"""\[\[(image|File|Category):%s\]\]|
        \[\[[^|^\]]+\||
        \[\[|
        \]\]|
        \'{2,5}|
        (<s>|<!--)[\s\S]+(</s>|-->)|
        {{[\s\S\n]+?}}|
        {\|[\s\S\n]+?\|}|    #Tables {| class="wikitable" ... |}
        <ref[^<]+?/>|        #This excluded the case <ref ...<ref/> .../>
        <ref[\s\S]+?</ref>|
        </?(blockquote)>|
        ={1,6}"""%paren_matcher(3), re.VERBOSE)

display_math_regex = re.compile(
        r"""^:\s*<math>(.*?)</math>$  #Display Math starts with a colon
         """, re.X|re.S|re.M)

inline_math_regex = re.compile(r"""<math>.*?</math>""", re.X)

# Remove the nonbreaking spaces 
spaces_regex = re.compile(r"&nbsp;")

inline_string = '_inline_math_'
display_string = '_display_math_'



def loads(wiki, compress_spaces=None):
    '''
    Parse a string to remove and replace all wiki markup tags
    '''
    # The format is (regex, string)
    # every match of the regular expression is substituted with the 
    # string value
    regex_list = [(PRE, inline_string), 
                    (RE, ''),
                    (display_math_regex, display_string),
                    (inline_math_regex, inline_string),
                    (spaces_regex, ' ')]
    # reduce uses the format acum = func(acum, parameter)
    # so the next function swaps the values 
    sub_fun = lambda w,P: re.sub(P[0], P[1], w)
    result = reduce(sub_fun, regex_list, wiki)


    if compress_spaces:
        result = re.sub(r' +', ' ', result)

    return html.unescape(result)


def load(stream, compress_spaces=None):
    '''
    Parse the content of a file to un-wikified text
    '''
    return loads(stream.read(), compress_spaces=compress_spaces)
