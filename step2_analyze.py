import os
import re
import collections
import matplotlib.pyplot as plt

years = list(range(2013, 2021 + 1))
hists = []
for year in years:
    # get titles of cvpr iccv for this year
    titles = []
    fn = f'CVPR{year}.txt'
    if os.path.isfile(fn):
        with open(fn, 'r', encoding='utf8') as f:
            titles += f.readlines()
    fn = f'ICCV{year}.txt'
    if os.path.isfile(fn):
        with open(fn, 'r', encoding='utf8') as f:
            titles += f.readlines()

    assert len(titles) > 0

    # merge titles into long text, normalize, split into words
    titles = ' '.join(titles)
    titles = re.sub('[^0-9a-zA-Z]+', ' ', titles).strip()
    titles = titles.split()
    titles = list(map(lambda x: x.lower(), titles))

    # hist
    titles = list(filter(
        lambda x: x not in ['for', 'a', 'and', 'of', 'with', 'in', 'using', 'from', 'to', 'the', 'based', 'by', 'on',
                            'via'],
        titles))
    hist = collections.defaultdict(float, collections.Counter(titles).most_common())
    for k in hist:
        hist[k] = hist[k] / len(titles)
    # print(hist)
    # print(sum(hist.values()))
    hists.append(hist)

common_keys = set()
for hist in hists:
    common_keys.update(hist.keys())

trends = {}
for key in common_keys:
    trends[key] = []
    for hist in hists:
        trends[key].append(hist[key])
# trends = collections.OrderedDict(sorted(trends.items(), key=lambda kv: sum(kv[1]) / len(kv[1]), reverse=True))
trends = collections.OrderedDict(sorted(trends.items(), key=lambda kv: kv[1][-1], reverse=True))

fid_id = 0
plt.get_current_fig_manager().full_screen_toggle()
for k, v in trends.items():
    fid_id += 1
    if fid_id > 4 * 5:
        break
    plt.subplot(4, 5, fid_id)

    plt.plot(years, v)
    plt.title(k)
plt.tight_layout()
plt.show()
