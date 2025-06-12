import os
import csv
from pathlib import Path
from typing import List, Dict

import openai
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

CATALOG_PATH = Path(__file__).resolve().parent.parent / 'data' / 'product_catalog.csv'
FAQ_PATH = Path(__file__).resolve().parent.parent / 'faq'

_model = SentenceTransformer('all-MiniLM-L6-v2')


def _load_products() -> List[Dict[str, str]]:
    products = []
    with open(CATALOG_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append(row)
    return products


def _build_index(items: List[str]):
    embeddings = _model.encode(items, convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, embeddings


def _search_index(query: str, index, items: List[Dict[str, str]], k=3):
    q_emb = _model.encode([query], convert_to_numpy=True)
    _, idx = index.search(q_emb, k)
    return [items[i] for i in idx[0]]


def _load_faqs() -> List[Dict[str, str]]:
    faqs = []
    for md in FAQ_PATH.glob('*.md'):
        lines = md.read_text(encoding='utf-8').strip().splitlines()
        if not lines:
            continue
        question = lines[0].lstrip('# ').strip()
        answer = '\n'.join(lines[1:]).strip()
        faqs.append({'question': question, 'answer': answer})
    return faqs


def answer_question(question: str) -> str:
    products = _load_products()
    product_texts = [p['name'] + ' ' + p.get('description', '') for p in products]
    prod_index, _ = _build_index(product_texts)
    top_products = _search_index(question, prod_index, products)

    faqs = _load_faqs()
    faq_texts = [f["question"] + ' ' + f['answer'] for f in faqs]
    faq_index, _ = _build_index(faq_texts)
    faq_match = _search_index(question, faq_index, faqs, k=1)[0]

    prompt = [
        {
            'role': 'system',
            'content': 'You are RetailBot, an assistant that helps customers find products and answers questions.'
        },
        {
            'role': 'user',
            'content': (
                f"User question: {question}\n\n"
                f"Relevant products: {', '.join(p['name'] for p in top_products)}\n"
                f"FAQ match: {faq_match['question']} - {faq_match['answer']}\n"
                "Answer:"
            )
        }
    ]

    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=prompt)
    return response.choices[0].message['content'].strip()


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('Usage: python -m retailbot.chatbot "<question>"')
        sys.exit(1)

    q = sys.argv[1]
    print(answer_question(q))
