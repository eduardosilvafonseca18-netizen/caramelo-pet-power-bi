"""Gera a apresentação do README usando os resumos extraídos do PBIX final."""
from pathlib import Path
import csv

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
NAVY, AMBER, MUTED, BACKGROUND = '#0B2545', '#F4A72C', '#5C6B7A', '#EEF1F5'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'text.color': NAVY,
                     'axes.labelcolor': MUTED, 'xtick.color': MUTED,
                     'ytick.color': MUTED, 'font.size': 12})

def read_csv(name):
    with (ROOT / 'dados' / name).open(encoding='utf-8', newline='') as source:
        return list(csv.DictReader(source))

def br(number, digits=2):
    return f'{number:,.{digits}f}'.replace(',', '_').replace('.', ',').replace('_', '.')

annual = read_csv('resumo_anual.csv')
countries = read_csv('resumo_paises.csv')
years = [int(row['Ano']) for row in annual]
revenue = [float(row['Receita']) for row in annual]
profit = [float(row['Lucro']) for row in annual]
total = sum(revenue)
total_profit = sum(profit)
growth = (revenue[-1] / revenue[-2] - 1) * 100
concentration = sum(float(row['Receita']) for row in countries[:2]) / total * 100

fig = plt.figure(figsize=(16, 9), facecolor=BACKGROUND)
fig.text(.05, .942, 'CARAMELO PET', fontsize=28, weight='bold')
fig.text(.05, .898, 'Análise comercial  /  Receita, rentabilidade e crescimento', fontsize=14, color=MUTED)
fig.text(.95, .942, '2014 — 2017', ha='right', fontsize=15, weight='bold')
fig.text(.95, .903, '54.530 vendas · 7 países', ha='right', fontsize=12, color=MUTED)

cards = [
    ('RECEITA', br(total / 1e6) + ' mi', 'Líquida de desconto'),
    ('LUCRO BRUTO', br(total_profit / 1e6) + ' mi', 'Receita menos custo dos produtos'),
    ('MARGEM BRUTA', br(total_profit / total * 100) + '%', 'Lucro bruto / receita'),
    ('CRESCIMENTO', '+' + br(growth) + '%', 'Receita de 2017 × 2016'),
]
for i, (label, value, detail) in enumerate(cards):
    x = .05 + i * .23
    fig.add_artist(FancyBboxPatch((x, .706), .21, .153, transform=fig.transFigure,
                   boxstyle='round,pad=0.009,rounding_size=0.014',
                   facecolor='white', edgecolor='none', zorder=0))
    fig.text(x + .013, .826, label, fontsize=11, weight='bold', color=MUTED)
    fig.text(x + .013, .771, value, fontsize=29, weight='bold')
    fig.text(x + .013, .730, detail, fontsize=9.5, color=MUTED)

for x, width in [(.05, .445), (.515, .435)]:
    fig.add_artist(FancyBboxPatch((x, .221), width, .440, transform=fig.transFigure,
                   boxstyle='round,pad=0.009,rounding_size=0.014',
                   facecolor='white', edgecolor='none', zorder=0))

fig.text(.073, .622, 'Evolução anual', fontsize=17, weight='bold')
fig.text(.073, .592, 'Receita e lucro bruto · milhões', fontsize=11, color=MUTED)
ax = fig.add_axes([.088, .284, .372, .263])
ax.plot(years, [v / 1e6 for v in revenue], color=AMBER, linewidth=3.5, marker='o', markersize=7, label='Receita')
ax.plot(years, [v / 1e6 for v in profit], color=NAVY, linewidth=3, marker='o', markersize=6, label='Lucro bruto')
ax.set_xticks(years)
ax.set_ylim(0, 27)
ax.set_yticks([0, 5, 10, 15, 20, 25])
ax.grid(axis='y', color='#E8EDF3')
ax.set_axisbelow(True)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(axis='both', length=0, pad=8)
ax.legend(loc='upper left', frameon=False, ncol=2, fontsize=10)
ax.annotate(br(revenue[-1] / 1e6), (years[-1], revenue[-1] / 1e6),
            xytext=(-8, 11), textcoords='offset points', ha='right', weight='bold', fontsize=11)
ax.annotate(br(profit[-1] / 1e6), (years[-1], profit[-1] / 1e6),
            xytext=(-8, -22), textcoords='offset points', ha='right', weight='bold', fontsize=11)

fig.text(.539, .622, 'Onde a receita se concentra', fontsize=17, weight='bold')
fig.text(.539, .592, 'Receita por país · milhões', fontsize=11, color=MUTED)
ax2 = fig.add_axes([.600, .271, .325, .281])
amounts = [float(row['Receita']) / 1e6 for row in countries]
bars = ax2.barh([row['País'] for row in countries], amounts,
               color=[AMBER if i < 2 else NAVY for i in range(len(countries))], height=.64)
ax2.invert_yaxis()
ax2.set_xlim(0, 28)
ax2.set_xticks([0, 10, 20])
ax2.grid(axis='x', color='#E8EDF3')
ax2.set_axisbelow(True)
for spine in ax2.spines.values():
    spine.set_visible(False)
ax2.tick_params(axis='both', length=0, pad=8, labelsize=10)
for bar, amount in zip(bars, amounts):
    ax2.text(amount + .55, bar.get_y() + bar.get_height() / 2,
             br(amount), va='center', fontsize=10, weight='bold')

fig.text(.05, .156, br(concentration, 1) + '% da receita vem de Argentina e Colômbia.',
         fontsize=16, weight='bold')
fig.text(.05, .116, 'Concentração comercial relevante para acompanhar ao lado do mix de produtos e da margem.',
         fontsize=12, color=MUTED)
fig.text(.05, .052, 'Resumo analítico gerado a partir dos dados do PBIX · Unidade monetária não informada na base',
         fontsize=9.5, color=MUTED)
fig.text(.95, .052, 'Eduardo da Silva Fonseca', ha='right', fontsize=10, color=MUTED)

output = ROOT / 'docs/assets/visao-geral.png'
output.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(output, dpi=125, facecolor=BACKGROUND)
plt.close(fig)
print(output)
