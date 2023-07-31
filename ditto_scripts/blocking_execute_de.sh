python ./blocking_ditto/blocker.py \
  --input_path ../ditto_prep/data/ \
  --left_fn scm_colval_de.txt \
  --right_fn coypu_colval_de.txt \
  --output_fn candidates_fuzzy_de.jsonl \
  --model_fn  albert-large-v1 \
  --k 10