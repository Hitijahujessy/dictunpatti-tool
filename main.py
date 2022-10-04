import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd

df = pd.DataFrame()
i = 1


for x in range(127):

    url = 'https://dict.unpatti.ac.id/?page=' + str(i)

    print('importing page', str(i))

    table = pd.DataFrame(pd.read_html(url)[1])
    table.drop(table.tail(7).index,
            inplace=True)
    table.dropna()
    df = df.append(table)
    #print(data)

    i += 1

# dictionairy = pd.DataFrame(data)
# with pd.option_context('display.max_rows', None,
#                        'display.max_columns', None,
#                        'display.precision', 100,
#                        ):
#
#     print('\n', dictionairy)
#
df.to_csv('hotumese.csv', index=False)