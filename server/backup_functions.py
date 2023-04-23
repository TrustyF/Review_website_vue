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
