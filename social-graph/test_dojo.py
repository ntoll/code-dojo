"""
Nosetests for dojo.py

see http://somethingaboutorange.com/mrl/projects/nose/
"""
import dojo

from twitter.api import Twitter

def create_dot_file_test():
    # A very contrived directed graph as a list...
    edges = [
            [1, 2], 
            [1, 3],
            [1, 4],
            [1, 5],
            [1, 6],
            [2, 1],
            [2, 7],
            [3, 2],
            [3, 4],
            [3, 7],
            [4, 1],
            [4, 7],
            [5, 6],
            [5, 7],
            [6, 1],
            [7, 6],
            ]
    # Test without root node
    expected = 'digraph G { 1 -> 2; 1 -> 3; 1 -> 4; 1 -> 5; 1 -> 6; 2 -> 1; 2'\
            ' -> 7; 3 -> 2; 3 -> 4; 3 -> 7; 4 -> 1; 4 -> 7; 5 -> 6; 5 -> 7; 6'\
            ' -> 1; 7 -> 6; }'
    assert expected == dojo.create_dot_file(edges)

    # Test with root node
    expected = 'digraph G { node [shape = doublecircle]; 3; node [shape ='\
            ' circle]; 1 -> 2; 1 -> 3; 1 -> 4; 1 -> 5; 1 -> 6; 2 -> 1; 2 -> 7;'\
            ' 3 -> 2; 3 -> 4; 3 -> 7; 4 -> 1; 4 -> 7; 5 -> 6; 5 -> 7; 6 -> 1;'\
            ' 7 -> 6; }'
    assert expected == dojo.create_dot_file(edges, root_node=3)

def create_styled_dot_file_test():
    # Some more contrived examples
    users = {
        'ntoll': {'following': 53, 'followers': 172, 'full name': 'Nicholas Tollervey'}, 
        'bob': {'full name': 'Bob T.Builder'}, 
        'fred': {'full name': 'Fred Blogs'}
        }
    edges = [
            ['ntoll', 'fred'], 
            ['fred', 'ntoll'], 
            ['ntoll', 'bob'], 
            ['fred', 'bob'],
            ]
    expected = 'digraph G { node [ fontname = "Helvetica" fontsize = 8 shape = "plaintext" ] ntoll [label=< <table border="0" cellborder="0" cellspacing="0" bgcolor="#CCCCCC"> <tr> <td colspan="2" cellpadding="2" align="center" bgcolor="#33CCFF"> <font face="Helvetica Bold">ntoll</font> </td> </tr> <tr> <td align="left" cellpadding="2"><font face="Helvetica Bold">following</font></td> <td align="left" cellpadding="2">53</td> </tr>\n<tr> <td align="left" cellpadding="2"><font face="Helvetica Bold">followers</font></td> <td align="left" cellpadding="2">172</td> </tr>\n<tr> <td align="left" cellpadding="2"><font face="Helvetica Bold">full name</font></td> <td align="left" cellpadding="2">Nicholas Tollervey</td> </tr> </table> >]\nbob [label=< <table border="0" cellborder="0" cellspacing="0" bgcolor="#CCCCCC"> <tr> <td colspan="2" cellpadding="2" align="center" bgcolor="#33CCFF"> <font face="Helvetica Bold">bob</font> </td> </tr> <tr> <td align="left" cellpadding="2"><font face="Helvetica Bold">full name</font></td> <td align="left" cellpadding="2">Bob T.Builder</td> </tr> </table> >]\nfred [label=< <table border="0" cellborder="0" cellspacing="0" bgcolor="#CCCCCC"> <tr> <td colspan="2" cellpadding="2" align="center" bgcolor="#33CCFF"> <font face="Helvetica Bold">fred</font> </td> </tr> <tr> <td align="left" cellpadding="2"><font face="Helvetica Bold">full name</font></td> <td align="left" cellpadding="2">Fred Blogs</td> </tr> </table> >] ntoll -> fred; fred -> ntoll; ntoll -> bob; fred -> bob; }'
    assert expected == dojo.create_styled_dot_file(users, edges)


def get_list_of_friends_test():
    twitter = Twitter('lpdojo', 'asdfasdf')
    twitterer = 'lpdojo'
    friends = dojo.get_list_of_friends(twitter, twitterer)
    assert isinstance(friends[0], int)  
