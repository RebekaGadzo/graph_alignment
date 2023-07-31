SERVER_CONFIG = {
    'base_url': 'localhost',
    'port': 8000,
    'task': {
        'full': {
             'DE': 'SCM-COYPU/FULL/DE',
            # 'US': 'SCM-COYPU/FULL/US',
            # 'CN': 'SCM-COYPU/FULL/CN',
        },
        'no_loc': {
             'DE': 'SCM-COYPU/UNPARSED/DE',
            # 'US': 'SCM-COYPU/UNPARSED/US',
            # 'CN': 'SCM-COYPU/UNPARSED/CN',
        }
    },
    'checkpoint_path': 'checkpoints/',
    'language_model': 'distilbert',
    'use_gpu': False,
    'use_fp16': False,
    'max_len': 64,
    'input_folder': './input/queries/',
    'output_folder': './output/queries/',
}