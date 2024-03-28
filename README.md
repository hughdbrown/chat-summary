# Purpose
Given chat data (from a webinar, say), summarize the text in several ways and make a navigable HTML file.

# Execution
```
$ ./chat-summary > chat-summary.html
$ open chat-summary.html
```

# Requirements
User must provide a file in the same directory named `chat_data.py` that exposes a global variable named `data` that is a multiline string whose lines are repeating sequences of blank line, user name, and chat text.
