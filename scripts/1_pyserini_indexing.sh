python -m pyserini.index.lucene \
  --collection JsonCollection \
  --input "[PATH-TO-CORPUS]" \
  --index "[PATH-TO-SAVE-INDEXES]" \
  --generator DefaultLuceneDocumentGenerator \
  --threads 1 \
  --storePositions --storeDocvectors --storeRaw

