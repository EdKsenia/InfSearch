import pymorphy2

tokens = ''
with open('tokens2.txt', encoding="utf-8") as file:
    tokens = [row.strip() for row in file]

lemms = {}
for token in tokens:
    morph = pymorphy2.MorphAnalyzer(lang='ru')
    # print(tokens[i])
    norm_form=morph.parse(token)[0].normal_form
    if norm_form in lemms.keys():
        lemms[norm_form].append(token)
    else:
        lemms[norm_form] = [token]
print('Dictionary was created')
with open('lemms.txt', "w", encoding="utf-8") as f:
    for key in lemms:
        f.write(key+': ')
        for token in lemms[key]:
            f.write(token + ' ')
        f.write('\n')
print(lemms)
print(len(lemms))


