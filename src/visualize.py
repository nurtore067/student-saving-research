"""Two compact figures with physical units and uncertainty."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.process_data import load_logs, summarize

ROOT = Path(__file__).resolve().parents[1]
COLORS = ['#0072B2','#D55E00']


def make_figures(logs, summary):
    out = ROOT/'reports/figures'
    out.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    fig, ax = plt.subplots(figsize=(7,4.5),layout='constrained')
    for method,color,marker,style in zip(['Baseline','Proposed'],COLORS,['o','s'],['-','--']):
        d = summary[summary.method == method].sort_values('load')
        ax.errorbar(d.load,d.median_ms,
                    yerr=[d.median_ms-d.ci_low_ms,d.ci_high_ms-d.median_ms],
                    label=method,color=color,marker=marker,linestyle=style,capsize=4)
    ax.set(xlabel='Batch size (profiles)',ylabel='Batch latency (ms; log scale)',
           title='Guidance execution: median and 95% bootstrap CI',yscale='log')
    ax.set_xticks(sorted(summary.load.unique()))
    ax.legend()
    ax.grid(alpha=.2)
    save(fig,out/'fig1_latency_vs_load')
    fig2, ax = plt.subplots(figsize=(7,4.5),layout='constrained')
    load = int(summary.load.max())
    for position,(method,color,marker) in enumerate(zip(['Baseline','Proposed'],COLORS,['o','s']),start=1):
        values=logs.loc[(logs.phase=='benchmark') & logs.ok & (logs.load==load) & (logs.method==method),'latency_ms']
        ax.boxplot([values],positions=[position],widths=.4,patch_artist=True,
                   boxprops={'facecolor':color,'alpha':.4},medianprops={'color':'black'},
                   flierprops={'marker':'.','markersize':3,'alpha':.4})
        row=summary[(summary.load==load)&(summary.method==method)].iloc[0]
        ax.errorbar(position+.27,row.median_ms,
                    yerr=[[row.median_ms-row.ci_low_ms],[row.ci_high_ms-row.median_ms]],
                    color=color,marker=marker,capsize=5,label=f'{method}: median 95% CI')
    ax.set(xticks=[1,2],xticklabels=['Baseline','Proposed'],ylabel='Batch latency (ms; log scale)',
           yscale='log',title=f'Latency distribution for {load} profiles')
    ax.set_xlabel('Guidance method (category)')
    ax.legend(fontsize=9)
    ax.grid(axis='y',alpha=.2)
    save(fig2,out/'fig2_distribution_boxplot')
    plt.close('all')


def save(fig,path):
    fig.savefig(str(path)+'.png',dpi=300)
    fig.savefig(str(path)+'.pdf')


if __name__ == '__main__':
    logs=load_logs()
    make_figures(logs,summarize(logs))
