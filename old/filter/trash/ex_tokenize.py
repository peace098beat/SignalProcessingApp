import tokenize

reader = open('yu.py').readline
tokens = tokenize.generate_tokens(reader)
