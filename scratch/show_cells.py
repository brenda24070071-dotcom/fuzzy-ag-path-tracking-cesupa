import json

nb = json.load(open('fuzzy_path_tracking.ipynb', encoding='utf-8'))
for i in [6, 8, 25]:
    cell = nb['cells'][i]
    src = ''.join(cell['source'])
    print(f"========== Cell {i} ==========")
    print(src)
    print()
