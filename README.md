# Word-Level Text Generation (NLG)

**Natural Language Generation (NLG)** or Text Generation is a subfield of Natural Language Processing (NLP). Its goal is to generate meaningful phrases and sentences in the form of human-written text. It has a wide range of use cases: writing long form content (eg reports, articles), product descriptions, social media posts, chatbots etc.

The goal of this project is to generate text of fairy tale using different approaches: Markov Chain, LSTM neural network and Transformers (GPT-2). Models are going to be implemented on a word-level. The content of fairy tales scraped from the Internet will be used as a text corpus.

------

**Table of contents:**

1. **Text Generation with Markov Chain** - simple, stochastic model which predicts the next word solely based on the previous sequence.
2. **Text Generation with Neural Networks (LSTM)** - the model stors in the memory the previous words and based on it, it calculated the probability of the next word
3. **Text Generation with Transformers (GPT-2)** - the transformer uses a "self-attention" mechanism to predict the next word in a sentence by focusing on words that were previously seen in the model and that are related to the predicted word

------

**Source of fairy tales content:**

* https://www.pitt.edu/~dash/folktexts.html
* [Kaggle Fairy Tales Dataset](https://www.kaggle.com/cuddlefish/fairy-tales)

