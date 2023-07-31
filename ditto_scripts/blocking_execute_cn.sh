python ./blocking_ditto/blocker.py \
  --input_path ../ditto_prep/data/ \
  --left_fn scm_colval_cn.txt \
  --right_fn coypu_colval_cn.txt \
  --output_fn candidates_fuzzy_cn.jsonl \
  --model_fn  "../blocking_ditto/model_fuzzy_cn.pth" \
  --k 10