# def init_sorted():
#     def load_init():
#         print('loading init')
#         with open('../client/public/assets/movie_db_lib.json', 'rb') as infile:
#             data = json.load(infile)
#
#         for entry in data:
#             unsorted_database.insert(entry)
#
#     unsorted_database = TinyDB(unsorted_json_file_path)
#     for i in reversed(range(1, 11)):
#         curr_table = sorted_database.table(f'ranked_{i}')
#         records = unsorted_database.search(where('my_rating') == str(i))
#         curr_table.insert_multiple(records)

# def add_date_added():
#     with open(r"C:\Users\Arthur\Downloads\ratings.csv") as infile:
#         reader = csv.reader(infile, delimiter=",", quotechar='"')
#         data_read = [row for row in reader]
#         data_read = data_read[1:]
#
#     for entry in data_read:
#         date_rated = entry[2]
#         title = entry[3]
#         # print(title, date_rated)
#
#         for table in sorted_database.tables():
#             for movie in sorted_database.table(table).all():
#                 if movie['title'] == title:
#                     query = Query().title == title
#                     document = sorted_database.table(table).search(query)[0]
#                     document.update({"date_rated": date_rated})
#                     sorted_database.table(table).update(document, query)
#                     # print(movie)
#         # break

# def add_missing_data():
#     api_key = '063ccf740a391dee9759aaa3564661c2'
#     count = 0
#     for movie in sorted_database.table('movies'):
#         # print(movie)
#         try:
#             imdb_id = (movie['imdb_url'].split('/')[4])
#         except:
#             continue
#
#         print(movie['title'], imdb_id)
#
#         if count < 600:
#             count += 1
#             continue
#
#         simple_response = urllib.request.urlopen(
#             f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={api_key}&language=en-US&external_source=imdb_id")
#         simple_data = json.load(simple_response)
#         simple_data = simple_data[f"{movie['media_type']}_results"][0]
#
#         full_response = urllib.request.urlopen(
#             f"https://api.themoviedb.org/3/{movie['media_type']}/{simple_data['id']}?api_key={api_key}&language=en-US&append_to_response=credits,images&include_image_language=en,null")
#
#         query = Query().imdb_url == str(movie['imdb_url'])
#         full_response = json.load(full_response)
#         original = sorted_database.table('movies').search(query)[0]
#
#         sorted_database.table('movies').update((full_response | original), query)

# def delete_data():
# for movie in sorted_database.table('movies'):
#     query = Query().title == str(movie['title'])
#
#     try:
#         sorted_database.table('movies').update_multiple([
#             (operations.delete('adult'), query),
#             (operations.delete('belongs_to_collection'), query),
#             (operations.delete('budget'), query),
#             (operations.delete('credits'), query),
#             (operations.delete('homepage'), query),
#             (operations.delete('production_companies'), query),
#             (operations.delete('production_countries'), query),
#             (operations.delete('revenue'), query),
#             (operations.delete('spoken_languages'), query),
#             (operations.delete('status'), query),
#             (operations.delete('tagline'), query),
#             (operations.delete('video'), query),
#         ])
#     except KeyError:
#         pass
#
#     # del movie['images']['backdrops']
#     # del movie['images']['logos']
#     # movie['images']['posters'] = movie['images']['posters'][:5]
#     # sorted_database.table('movies').update()
#
#     # pprint.pprint(sorted_database.table('movies').search(query))
#     # break