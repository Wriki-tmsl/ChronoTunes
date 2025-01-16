import pandas as pd
import random
def find_similar_songs(name):
    # Find songs most similar to another song
    sim_df_names=pd.read_csv("similarity.csv",index_col=1)
    #df=sim_df_names.sort_values(by=[name],ascending = False)
    df=sim_df_names["Song Name"]
    sample_df = df.sample(n=15,random_state=66)
    sample_df.to_csv("playlist.csv",index=["Song Name"])
    print(sample_df)
    #series = sim_df_names.sort_values(by=[name],ascending = False)
    #select_random_songs(series)

find_similar_songs("Dine Dine Khoshiya Poribe") 