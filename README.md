# Korean Benchmark for Legal Language Understanding (KBL)
- This is an official repository for the KBL dataset from [LBox](https://lbox.kr/v2).
- The work will be presented at [EMNLP 2024](https://2024.emnlp.org/) Findings and the [NLLP Workshop](https://nllpw.org/workshop/).
- The paper is available from [here](https://arxiv.org/abs/2410.08731).

# To Do
- [x] [Released the benchmark on the Hugging Face Hub](https://huggingface.co/datasets/lbox/kbl)
  - [x] To access the dataset for RAG tasks, visit [here](https://huggingface.co/datasets/lbox/kbl-rag)
- [x] [Released zero-shot task `yaml` files](https://github.com/lbox-kr/lm-evaluation-harness-kbl)
- [x] [Published the evaluation results.](https://huggingface.co/datasets/lbox/kbl-emnlp24-evaluation-results/tree/main)
- [x] Release the Korean statutes and precedents corpus for RAG experiment.

- [x] [Release the RAG task `yaml` files](https://huggingface.co/datasets/lbox/kbl).
  - Currently, due to technical difficulty, evaluating LLMs under the RAG setting is possible with given retrived documents using a [custom branch of `lm-eval-harness`](https://github.com/lbox-kr/lm-evaluation-harness-kbl).

  - LRAGE, a RAG evaluation tool specifically tailored for the legal domain, is under active construction. The full features will be supported around Dec 15 2024. Please check the tool from [here](https://github.com/hoorangyee/LRAGE/tree/main).
- [x] Make the yaml files and corresponding utils available in [`lm-evaluation-harness` repository](https://github.com/EleutherAI/lm-evaluation-harness) 
  - [Done](https://github.com/EleutherAI/lm-evaluation-harness/pull/2493#issuecomment-2480736242)
- [x] Share the data processing script for RAG experiments.
- [x] Present the paper at EMNLP 2024.
- [ ] Release yaml files for `multiple_choice` type evaluations.

# Datasets
## Benchmarks
### How to load examples
```python
from pprint import pprint
import datasets

data = datasets.load_dataset("lbox/kbl", data_files={"test": [FILE_PATH]})
# Example
# data = datasets.load_dataset('lbox/kbl', data_files={"test": "knowledge/kbl_legal_concept_qa_v0.1.json"})["test"]
pprint(data[0])

```
## Corpus
- Korean statutes (220,160 articles. Dumped at Nov2024) 
- Korean precedents (From [LBox-Open](https://github.com/lbox-kr/lbox-open))

### How to load corpus
```python
from pprint import pprint
import datasets

# Load statutes corpus
data = datasets.load_dataset('lbox/kbl-rag', data_files={"train": "corpus/statutes.jsonl"})["train"]

# Load precedents corpus
# data = datasets.load_dataset('lbox/kbl', data_files={"train": "corpus/precedents.jsonl"})["train"]

# Load precedents and statutes corpus
# data = datasets.load_dataset('lbox/kbl', data_files={"train": "corpus/precedents_and_statutes.jsonl"})["train"]
pprint(data[0])

```



# Citation
```
@inproceedings{kim2024kbl,
    title = "Developing a Pragmatic Benchmark for Assessing {K}orean Legal Language Understanding in Large Language Models",
    author = {Yeeun Kim and Young Rok Choi and Eunkyung Choi and Jinhwan Choi and Hai Jin Park and Wonseok Hwang},
    editor = "Al-Onaizan, Yaser  and
      Bansal, Mohit  and
      Chen, Yun-Nung",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2024",
    month = nov,
    year = "2024",
    address = "Miami, Florida, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.findings-emnlp.319",
    pages = "5573--5595",
}
```
