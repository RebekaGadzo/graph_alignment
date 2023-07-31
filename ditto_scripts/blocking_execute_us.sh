python ./blocking_ditto/blocker.py \
  --input_path ../ditto_prep/data/ \
  --left_fn scm_colval_us.txt \
  --right_fn coypu_colval_us.txt \
  --output_fn candidates_fuzzy_us.jsonl \
  --model_fn  "../blocking_ditto/model_fuzzy_us.pth" \
  --k 10