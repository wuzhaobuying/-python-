import pandas as pd

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table('datasets/movielens/users.dat', sep='::', header=None, names=unames, )

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('datasets/movielens/ratings.dat', sep='::', header=None, names=rnames)

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('datasets/movielens/movies.dat', sep='::', header=None, names=mnames)

print(users[:5])
print(ratings[:5])
print(movies[:5])
print(ratings)

data = pd.merge(pd.merge(ratings, users, on='user_id'), movies, on='movie_id')
print(data)
print(data.iloc[0])

mean_ratings = data.pivot_table('rating', index='title', columns='gender', aggfunc='mean')
print(mean_ratings[:5])

ratings_by_title = data.groupby('title').size()
print(ratings_by_title[:10])

active_titles = ratings_by_title.index[ratings_by_title >= 250]
print(active_titles)

mean_ratings = mean_ratings.loc[active_titles]
print(mean_ratings)

top_female_ratings = mean_ratings.sort_values(by='F', ascending=False)
print(top_female_ratings[:10])

mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
print(mean_ratings[:10])

sorted_by_diff = mean_ratings.sort_values(by='diff')
print(sorted_by_diff[:10])
print(sorted_by_diff[::-1][:10])

rating_std_by_title = data.groupby('title')['rating'].std()
rating_std_by_title = rating_std_by_title.loc[active_titles]
rating_std_by_title = rating_std_by_title.sort_values(ascending=False)[:10]
print(rating_std_by_title)