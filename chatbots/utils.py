from functools import wraps
import time
import re

import numpy as np
from langchain.embeddings import OpenAIEmbeddings


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


def split_text_into_sentences(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
    return sentences


def randomly_combine_sentences(sentences):
    return [sentences[i] + " " + sentences[i + 1] for i in range(0, len(sentences) - 1, 2)]


def combine_sentences_similarity(sentences):
    """
    The function will compares one sentence to the next one and determine if they are
    similar or not.
    If so, they are merged together.
    """
    embeddings_model = OpenAIEmbeddings()
    embeddings = embeddings_model.embed_documents(sentences)
    emb_idx = 0
    while emb_idx < (len(embeddings) - 1):
        product = np.dot(embeddings[emb_idx], embeddings[emb_idx + 1])
        if product >= 0.8:
            sentences = sentences[:emb_idx]
            sentences += [sentences[emb_idx] + " " + sentences[emb_idx + 1]]
            sentences += sentences[emb_idx + 2:]
            embeddings = embeddings_model.embed_documents(sentences)
        else:
            emb_idx += 1
    return sentences
