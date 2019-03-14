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

PRE = re.compile(r"""(?P<math>{{\s*(?:math|mvar)\s*\|)(.*?)(?(math)}}|)
                  """, re.X)

RE = re.compile(r"""\[\[(image|File|Category):[\s\S]+?\]\]|
        \[\[[^|^\]]+\||
        \[\[|
        \]\]|
        \'{2,5}|
        (<s>|<!--)[\s\S]+(</s>|-->)|
        {{[\s\S\n]+?}}|
        <ref>[\s\S]+</ref>|
        ={1,6}""", re.VERBOSE)

display_math_regex = re.compile(
        r"""^:\s*<math>(.*?)</math>$  #Display Math starts with a colon
         """, re.X|re.S|re.M)

inline_math_regex = re.compile(r"""<math>.*?</math>""", re.X)

inline_string = '_inline_math_'
display_string = '_display_math_'



def loads(wiki, compress_spaces=None):
    '''
    Parse a string to remove and replace all wiki markup tags
    '''
    wiki = PRE.sub(inline_string, wiki)
    result = RE.sub('', wiki)
    result = display_math_regex.sub('_display_math_', result)
    result = inline_math_regex.sub('_inline_math_', result)

    if compress_spaces:
        result = re.sub(r' +', ' ', result)

    return result


def load(stream, compress_spaces=None):
    '''
    Parse the content of a file to un-wikified text
    '''
    return loads(stream.read(), compress_spaces=compress_spaces)
