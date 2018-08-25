# -*- coding: utf-8 -*-
import sys
import re

# チェック元ファイル
f = open("testcopy.txt")
# 絵文字除去後のファイル
new_file = open('testcopy_rm_emoji.txt', 'a')

# 正規表現パターンを構築
emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
                           "]+", flags=re.UNICODE)

#(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)
#^[、|！|\s]*\n$
#^[0-9a-zA-Z|\s| -/:-@\[-~]+$

# １行ずつ処理
for line in f:
    print(line)
    new_file.write(emoji_pattern.sub(r'', line))

f.close();
new_file.close();