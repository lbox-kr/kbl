import json

import tqdm
from pyserini.search.lucene import LuceneSearcher


def stop_flag(idx, toy_size):
    # idx + 1 = length
    data_size = idx + 1
    if toy_size is not None:
        if toy_size <= data_size:
            return True
    else:
        return False


def save_json(data, path_save):
    with open(path_save, "w") as f:
        json.dump(data, f, ensure_ascii=False)


def load_json(fpath):
    with open(fpath) as f:
        return json.load(f)


def load_jsonl(fpath, toy_size=None, disable_tqdm=False):
    data = []
    with open(fpath) as f:
        for i, line in tqdm(enumerate(f), disable=disable_tqdm):
            try:
                data1 = json.loads(line)
            except:
                print(f"{i}th sample failed.")
                print(f"We will skip this!")
                print(line)
                data1 = None

            if data1 is not None:
                data.append(data1)
            if stop_flag(i, toy_size):
                break

    return data


class BM25Retriever:
    def __init__(self, path_index: str, title: str = None):
        self.searcher = LuceneSearcher(path_index)
        self.title = title

    def ask(self, query: str, top_k: int = 5):
        hits = self.searcher.search(query, k=top_k)
        retrieved_docs = []
        print("-----------------------------")
        for hit in hits:
            docid = hit.docid
            print(f"docid: {docid}")
            score = hit.score
            d = self.searcher.doc(docid)

            retrieved_doc = {
                "doc_id": docid,
                "score": score,
                "title": self.title,
                "passage": json.loads(d.raw())["contents"],
            }
            retrieved_docs.append(retrieved_doc)

        return {"results": retrieved_docs}  # for the consistency with lbox ai retreiver

    @staticmethod
    def gen_title(docid):
        if "statute" in docid:
            return "법령"
        elif "precedent" in docid:
            return "판례"
