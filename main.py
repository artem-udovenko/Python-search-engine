"""
Phrases search engine (PSE) is script that you need to find some specific phrases in text.
Its advantage is ability to find phrases in different grammar forms, moreover in any languages.
ATTENTION: The source text file should be in UTF-8 encoding!
"""

import re
import os


def words_select(string):
    words = re.split(r"\W+", string)
    return [word.lower() for word in filter(lambda x: x != '', words)]


def find(phrase, depth, volume):
    global SIZE, line_counter, black_mark
    long_string = list()
    for ind in range(SIZE):
        long_string += lines[ind]
    for i in range(len(long_string)):
        if long_string[i][1] in black_mark:
            continue
        if re.compile(phrase[0][:len(phrase[0]) - depth] + ".*").fullmatch(long_string[i][0]):
            suitable_phrase = ' '.join([pair[0] for pair in long_string[i:min(i + len(phrase), len(long_string))]])
            pattern = ' '.join([word[:len(word) - depth] + ".*" for word in phrase])
            if re.fullmatch(pattern, suitable_phrase):
                line_numbers = set([pair[1] for pair in long_string[i:i + len(phrase)]])
                black_mark = black_mark | line_numbers
                result[volume][depth].append(tuple([line_numbers,
                                            suitable_phrase,
                                            [text[num + SIZE - line_counter] for num in
                                             line_numbers]]))


phrase = tuple(input("Enter the phrase to find: ").lower().split())
DEPTH, SIZE = min(5, min([len(word) for word in phrase])), 10
files = list(filter(lambda x: re.fullmatch(r".*\.txt", x), os.listdir(os.path.dirname(os.path.abspath(__file__)))))
result = [[[] for i in range(DEPTH)] for j in range(len(files))]
black_mark = set()
with open(f"{os.path.dirname(os.path.abspath(__file__))}\\results\\{' '.join(phrase)}.txt", 'w', encoding="utf-8") as output:
    for num in range(len(files)):
        with open(f"{os.path.dirname(os.path.abspath(__file__))}\\{files[num]}", 'r', encoding="utf-8") as source:
            line, lines, line_counter = ' ', list(), SIZE + 1
            text = list()
            for i in range(SIZE):
                line = source.readline()
                text.append(line)
                lines.append([(word, i + 1) for word in words_select(line)])
            while line:
                for depth in range(DEPTH):
                    find(phrase, depth, num)
                line = source.readline()
                text.append(line)
                lines.append([(word, line_counter) for word in words_select(line)])
                text.pop(0)
                lines.pop(0)
                line_counter += 1
        output.write(f"VOLUME {num + 1} [{files[num]}]\n\n")
        for i in range(DEPTH):
            output.write(f"priority {i + 1}:\n")
            for pos in result[num][i]:
                output.write(f"\tline {','.join([str(num) for num in pos[0]])}: ")
                output.write(pos[1] + '\n')
                for l in pos[2]:
                    output.write("\t\t" + l + '\n')
        output.write('\n\n')