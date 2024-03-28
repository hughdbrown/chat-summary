#!/usr/bin/env python3
"""
Application to create navigable HTML page for chat data.

Data is expected to be a series of:
    blank line
    line with user name
    single line with text user submitted

The resulting HTML page gives:
- the original text without duplication. (The first usage had multiple copies of chat text copied from webinar.)
- user messages grouped together
- topics extracted with links to each topic's occurrence in chat
"""

from collections import defaultdict
import logging

# You need to provide this
# `data` is a multiline string in a python file named `chat_data.py`.
from chat_data import data

logging_args = {
    "format": "%(asctime)s %(levelname)s %(message)s",
    "level": logging.DEBUG,
    "datefmt": "%Y-%m-%d %H:%M:%S",
    "encoding": "utf-8",
}
logging.basicConfig(**logging_args)
logger = logging.getLogger(__name__)

# What they call `stop words` in NLP.
# Words that we do not attach much meaning to and which cannot be topics.
COMMON = {
    "the", "and", "a", "an", "no", "as", "than", "or", "but", "so",
    "much", "some", "little", "very", "many", "lot",
    "here", "there",
    "now", "never",
    "not", "also", "too",
    "like",
    "how", "why", "who", "when", "where", "what",
    "i", "me", "my", "mine",
    "you", "your", "yours",
    "he", "him", "his",
    "she", "her", "hers",
    "one", "one's",
    "it", "its",
    "we", "us", "our", "ours",
    "they", "them", "their", "theirs",
    "this", "that", "which", "these", "those",
    "someone", "something", "other",
    "for", "in", "at", "with", "to", "on", "from", "out", "about", "through", "up", "down", "over",
    "will", "is", "are", "do", "have", "had", "has", "was", "were", "done", "get",
    "got", "can", "be", "am", "getting", "got", "need", "been", "want", "should", "would", "go", "find", "give", "use", "must",
    "of", "if",
    "all", "some", "any", "only", "more", "just", "even", "by", "still",
    "-",
    "i've", "i'm", "you're", "don't", "it's",
    "thanks", "thank", "please",
}


def build_chat():
    people = set()
    lines = set()
    state = 0
    by_person = defaultdict(list)
    by_topic = defaultdict(list)
    person = None

    for i, line in enumerate(data.splitlines()):
        line = line.encode('ascii', 'ignore').rstrip().decode()
        if not line:
            state = 0
        elif state == 2:
            logger.error(f"Error in input: {i = } '{line}'") 
        elif state == 0:
            state = 1
            person = line
        elif state == 1:
            state = 2
            if line not in lines:
                by_person[person].append((i, line))
                lines.add(line)
                uniq_words_iter = {word.strip() for word in line.lower().split()}
                uniq_words = {word for word in uniq_words_iter if word not in COMMON}
                for word in uniq_words:
                    by_topic[word].append(i)

    by_line = {
        i: (p, line)
        for p, v in by_person.items()
        for (i, line) in v
    }

    return (by_line, by_person, by_topic) 


def chat_html(by_line, by_person, by_topic):
    """
    Generate an HTML page of the event. Summarize the chat by user
    """
    print("<html>")
    print("<head>")
    print("</head>")

    print("<body>")

    # Print all chat in order
    print(f"""<h1>Chat</h1>""")
    min_line, max_line = min(by_line), max(by_line)
    for i in range(min_line, max_line + 1):
        if (item := by_line.get(i)):
            person, line = item
            print(f"""
                <div id={i}>
                    {person}: <a href="#{person}">{line}</a>
                </div>
            """)

    # Summarize by person 
    print(f"""<h1>People</h1>""")
    for person, v in sorted(by_person.items()):
        print(f"""<div id="{person}">""")
        print(f"""<h3>{person}</h3>""")
        print("""<ol>""")
        for (i, line) in v:
            print(f"""<li><a href="#{i}">{line}</a></li>""")
        print("""</ol>""")
        print("</div>")

    # Summarize topics
    print(f"""<h1>Topics</h1>""")
    top_topics = sorted(by_topic.items(), key=lambda item: len(item[1]), reverse=True) 
    for topic, lines in top_topics[:50]:
        print(f"""<div>""")
        print(f"""<h3>{topic}</h3>""")
        for line in lines:
            print(f"""<a href="#{line}">{line}</a>""")
        print("</div>")

    print("</body>")
    print("</html>")


def main():
    (by_line, by_person, by_topic) = build_chat()
    chat_html(by_line, by_person, by_topic)
 

if __name__ == '__main__':
    main()
