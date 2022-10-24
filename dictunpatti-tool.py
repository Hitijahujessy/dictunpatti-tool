import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from time import sleep
import progressbar

def create_df():

    df = pd.DataFrame()
    i = 1
    n = 127
    bar = progressbar.ProgressBar(maxval=n, \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    for x in range(n):

        url = 'https://dict.unpatti.ac.id/?page=' + str(i)

        bar.update(x+1)
        sleep(0.1)

        
        table = pd.DataFrame(pd.read_html(url)[1])
        table.drop(table.tail(6).index,
                inplace=True)
        table.dropna()
        df = df.append(table)

        i += 1

    # dictionairy = pd.DataFrame(data)
    # with pd.option_context('display.max_rows', None,
    #                        'display.max_columns', None,
    #                        'display.precision', 100,
    #                        ):
    #
    #     print('\n', dictionairy)
    #
    df.to_csv('dict.csv', index=False)
    bar.finish() 

if __name__ == "__main__":
    
    input("Press enter to download dictionary.")
    create_df()
