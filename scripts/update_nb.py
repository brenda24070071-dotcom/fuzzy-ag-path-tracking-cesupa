import json

f = open(r'c:\Users\Kzar\Documents\Faculade\Fuzzy\fuzzy_path_tracking.ipynb', 'r', encoding='utf-8')
nb = json.load(f)
f.close()

for cell in nb['cells']:
    if cell['cell_type'] != 'code':
        continue
    src = ''.join(cell['source'])

    # 1. Add KDTree import
    if 'from scipy.interpolate import CubicSpline' in src and 'cKDTree' not in src:
        new_lines = []
        for line in cell['source']:
            new_lines.append(line)
            if 'from scipy.interpolate import CubicSpline' in line:
                new_lines.append('from scipy.spatial import cKDTree\n')
        cell['source'] = new_lines

    # 2. Fix Track class - use KDTree and 500 points
    if 'class Track:' in src:
        new_lines = []
        for line in cell['source']:
            if 'np.linspace(0, 1, 1000)' in line:
                line = line.replace('1000', '500')
            if 'self.rdx, self.rdy' in line:
                new_lines.append(line)
                new_lines.append('        self.tree = cKDTree(np.column_stack([self.rx, self.ry]))\n')
                continue
            if 'np.argmin' in line:
                line = line.replace(
                    'idx = np.argmin((self.rx - x)**2 + (self.ry - y)**2)',
                    '_, idx = self.tree.query([x, y])'
                )
            new_lines.append(line)
        cell['source'] = new_lines

    # 3. Fix universe resolution
    if 'np.arange(-50.0, 50.1, 0.1)' in src:
        new_lines = []
        for line in cell['source']:
            line = line.replace(
                'np.arange(-50.0, 50.1, 0.1)',
                'np.arange(-50.0, 50.1, 1.0)  # resolucao 1.0 (10x mais rapido)'
            )
            new_lines.append(line)
        cell['source'] = new_lines

f = open(r'c:\Users\Kzar\Documents\Faculade\Fuzzy\fuzzy_path_tracking.ipynb', 'w', encoding='utf-8')
json.dump(nb, f, ensure_ascii=False, indent=1)
f.close()
print('Notebook atualizado com sucesso!')
