import matplotlib.font_manager as fm
print([f.name for f in fm.fontManager.ttflist if 'Hei' in f.name or 'YaHei' in f.name])
