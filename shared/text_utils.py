import re


def split_into_sentences(text: str) -> list[str]:
    split_input = re.split(r'(?<=[.!?])[\s\n]+', text.strip())
    sentences = []
    for sentence in split_input:
        sentence = sentence.strip()
        if not sentence:
            continue
        sentences.append(sentence)
    return sentences
