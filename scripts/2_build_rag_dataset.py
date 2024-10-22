import argparse
import os
import sys
from copy import deepcopy
from pathlib import Path
import json

from tqdm import tqdm
from .utils import load_json, BM25Retriever, save_json


def func_answer_is_short(answer):
    if len(answer) > 40:
        return False
    short_answer_chars = set(["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ"])
    for char in short_answer_chars:
        if char in answer:
            return True
    return False


def main(retriever, path_kbl_data, retrieve_with_question_only=None, top_k=20):

    # Load data
    data = load_json(path_kbl_data)

    # Retrieve
    docss_retrieved = []
    data_rag = []
    for data1 in tqdm(data[:]):
        data1_rag = deepcopy(data1)
        question = data1["question"]
        q_and_as = deepcopy(question)

        auto_retrieve_with_question_only = False

        new_data1 = {}
        for k in ["A", "B", "C", "D", "E", "F", "G", "H"]:
            if k not in data1:
                continue
            q_and_as += f"\n{k}: {data1[k]}"
            if func_answer_is_short(data1[k]):
                auto_retrieve_with_question_only = True


        if retrieve_with_question_only is not None:
            print(f"Force retrieve_with_question_only: {retrieve_with_question_only}")
            auto_retrieve_with_question_only = retrieve_with_question_only

        if auto_retrieve_with_question_only:
            new_data1["question_and_individual_answers"] = {}
            for k in ["A", "B", "C", "D", "E", "F", "G", "H"]:
                if k not in data1:
                    continue
                new_data1["question_only"] = None
                new_data1["question_and_individual_answers"][k] = {}
                q_to_retriever = f"\n질문: {question}\n제시된 답변: {data1[k]}"
                new_data1["question_and_individual_answers"][k]["query"] = q_to_retriever
                new_data1["question_and_individual_answers"][k]["retrieved_docs"] = retriever.ask(q_to_retriever, top_k=top_k)
        else:
            new_data1["question_and_individual_answers"] = None
            new_data1["question_only"] = {}
            q_to_retriever = f"\n질문: {question}"
            new_data1["question_only"]["query"] = q_to_retriever
            new_data1["question_only"]["retrieved_docs"] = retriever.ask(q_to_retriever, top_k=top_k)


        docss_retrieved.append(new_data1)

        data1_rag["rag_data"] = new_data1
        data_rag.append(data1_rag)

    # Save
    save_dir = Path(path_kbl_data).parent / f"rag"
    fname_save = Path(path_kbl_data).stem + ".rag.json"
    os.makedirs(save_dir, exist_ok=True)
    save_json(data_rag, save_dir / fname_save)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path_kbl_data", type=str, default="")
    parser.add_argument("--retrieve_with_question_only", action="store_true")
    argv = parser.parse_args()

    path_index = "data/corpus/indexes/"
    retriever = BM25Retriever(path_index)

    main(retriever, argv.path_kbl_data, retrieve_with_question_only=argv.retrieve_with_question_only, top_k=20)
