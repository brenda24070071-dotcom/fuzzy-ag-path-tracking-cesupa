import json

nb = json.load(open('fuzzy_path_tracking.ipynb', encoding='utf-8'))
for i, cell in enumerate(nb['cells']):
    src = ''.join(cell['source'])
    preview = src[:120].replace('\n', ' | ')
    ct = cell['cell_type']
    print(f"Cell {i:2d} [{ct:8s}]: {preview}")
