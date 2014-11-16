import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

rc('font', **{'family': 'serif', 'serif': ['Palatino']})
rc('text', usetex=True)

lang_gdpcorr = [
    ('Python', -0.48493649677849227),
    ('Java', -0.41324914037655724),
    ('Haskell', -0.29808431723133072),
    ('JavaScript', -0.2667418269831574),
    ('C++', -0.2522813524612324),
    ('Clojure', -0.049654671767641156),
    ('C', -0.043328343161322704),
    ('Scheme', -0.022065549721714043),
    ('Ruby', 0.021250352627768899),
    ('OCaml', 0.10262292683825115)]

lang_unempcorr = [
    ('Java', 0.30774955040206092),
    ('Haskell', 0.26404413375817731),
    ('Clojure', 0.065582653798842205),
    ('Python', -0.0096011714242664366),
    ('C++', -0.039843278537423268),
    ('JavaScript', -0.060059854515008032),
    ('Scheme', -0.083913683167168102),
    ('Ruby', -0.14897872697899128),
    ('OCaml', -0.2137510973988315),
    ('C', -0.4785088152234489)]

lang_debtcorr = [
    ('Ruby', 0.29515176977774543),
    ('Clojure', 0.11568517827358332),
    ('Java', 0.043267123133860025),
    ('C++', 0.038824913242850846),
    ('Scheme', 0.0037523897625117183),
    ('JavaScript', -0.0064930569746978681),
    ('Haskell', -0.12868599769233782),
    ('C', -0.13746007000224705),
    ('Python', -0.32638056677591365),
    ('OCaml', -0.53847418569030447)]


def produce_figure(correlations, colorname, measure_name, filename):
    def autolabel(rects, ax):
        for rect in rects:
            height = rect.get_y()
            vertical = 'top'
            if height == 0:
                height = rect.get_height()
                vertical = 'bottom'
            ax.text(
                rect.get_x()+rect.get_width()/2.,
                1.05*height,
                '%.2f' % height,
                ha='center', va=vertical)

    N = len(correlations)
    xs = np.arange(N)
    width = 0.6

    fig, ax = plt.subplots()
    ys = [x[1] for x in correlations]
    rects = ax.bar(xs, ys, width, color=colorname, alpha=0.4)
    ax.set_ylabel(r'$\rho(%s,lang)$' % measure_name)
    ax.set_xticks(xs+width/2.0)
    plt.ylim([1.15*min(ys), 1.4*max(ys)])
    langs = []
    for lang, corr in correlations:
        if lang != 'JavaScript':
            langs.append(lang)
        else:
            langs.append('JS')
    ax.set_xticklabels(tuple(langs), rotation=45)
    autolabel(rects, ax)
    plt.savefig(filename)

#produce_figure(lang_gdpcorr, 'y', 'GDP', 'gdp_corr.png')
#produce_figure(lang_unempcorr, 'r', 'U', 'unemp_corr.png')
produce_figure(lang_debtcorr, 'b', 'D', 'debt_corr.png')
