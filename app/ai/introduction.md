What is RAG?

RAG (Retrieval-Augmented Generation) means that before an AI answers, it first searches through existing documents and information, and only responds based on that data.

In simple terms:

Instead of the model answering from its own memory, it first searches a library of texts, finds relevant content, and then generates an answer using that information.

What does this file do?

This file acts as the search and response engine in the project and performs three main tasks:

1. Storing documents

It receives the texts given to it.
It converts them into a format that a computer can compare in meaning (Embedding).
Then it stores them in memory.

2. Finding relevant texts

When a user asks a question, the question is also converted into the same format.
It then searches through all stored texts and finds the closest and most relevant ones.

3. Generating answers

It sends the relevant texts along with the question to the GPT model.
It asks the model to answer only based on those texts and even to cite the source of each part of the answer.
