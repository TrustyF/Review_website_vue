from sql_models.media_model import Media, Genre, Theme, Tag
from db_loader import db
import json


def insert_in_db():
    with open(r'D:\A_Main\A_Projects\WebDev\review_site\Review_website_server_BAK\database\movie_db.json',
              'r') as infile:
        movies = json.load(infile)['_default']
        print(f'{len(movies)} movies')

    with open(r'D:\A_Main\A_Projects\WebDev\review_site\Review_website_server_BAK\database\tv_db.json',
              'r') as infile:
        tv = json.load(infile)['_default']
        print(f'{len(tv)} tv')

    with open(r'D:\A_Main\A_Projects\WebDev\review_site\Review_website_server_BAK\database\anime_db.json',
              'r') as infile:
        anime = json.load(infile)['_default']
        print(f'{len(anime)} anime')

    with open(r'D:\A_Main\A_Projects\WebDev\review_site\Review_website_server_BAK\database\manga_db.json',
              'r') as infile:
        manga = json.load(infile)['_default']
        print(f'{len(manga)} manga')

    with open(r'D:\A_Main\A_Projects\WebDev\review_site\Review_website_server_BAK\database\game_db.json',
              'r') as infile:
        game = json.load(infile)['_default']
        print(f'{len(game)} game')

    with open(r'D:\A_Main\A_Projects\WebDev\review_site\Review_website_server_BAK\database\presets_db.json',
              'r') as infile:
        tags = json.load(infile)['_default']

    #  create genres
    for media in [movies, tv, anime, manga]:
        for entry in media:
            for genre in media[entry]['genres']:
                if not db.session.query(Genre).filter_by(name=genre).first():
                    new_genre = Genre(name=genre, origin=media[entry]['media_type'])
                    db.session.add(new_genre)

    # create themes
    for entry in game:
        for theme in game[entry]['themes']:
            print('theme', theme)
            if not db.session.query(Theme).filter_by(name=theme).first():
                new_theme = Theme(name=theme, origin=game[entry]['media_type'])
                db.session.add(new_theme)

        for genre in game[entry]['genres']:
            print('genre', genre)
            if not db.session.query(Genre).filter_by(name=genre).first():
                new_theme = Genre(name=genre, origin=game[entry]['media_type'])
                db.session.add(new_theme)

    #  create tags
    for media in [movies, tv, anime, manga, game]:
        for entry in media:
            for tag in media[entry]['tags'] or []:
                if not db.session.query(Tag).filter_by(name=tag['name']).first():
                    new_tag = Tag(
                        name=tag['name'],
                        overview=tag['description'],
                        image_path=tag['image'],
                        tier=tag['tier'],
                        origin=media[entry]['media_type']
                    )
                    db.session.add(new_tag)

    db.session.commit()

    # create media
    for media in [movies, tv, anime, manga, game]:
        print(f'test {len(media)}')
        for i, entry in enumerate(media):
            mov = media[entry]
            # print(mov['title'])

            new_mov = Media(
                name=mov['title'],
                overview=mov['overview'][:1000],
                poster_path=mov['poster_path'],
                media_type=mov['media_type'],
                release_date=mov['release_date'],

                user_rating=int(mov['my_rating']),
                public_rating=mov['vote_average'] if mov['media_type'] != 'game' else mov['vote_average'] / 10,

                external_id=None if 'imdb_id' not in mov else mov['imdb_id'],
                runtime=None if 'runtime' not in mov else mov['runtime'],
                episodes=None if 'episodes' not in mov else mov['episodes'],
                seasons=None if 'seasons' not in mov else mov['seasons'],
                content_rating=None if 'contentRating' not in mov else mov['contentRating'],
            )

            genres = []
            themes = []
            tags = []

            try:
                genres = [db.session.query(Genre).filter_by(name=x).first() for x in mov['genres']]
            except:
                pass
            try:
                themes = [db.session.query(Theme).filter_by(name=x).first() for x in mov['themes']]
            except:
                pass
            try:
                tags = [db.session.query(Tag).filter_by(name=x['name']).first() for x in mov['tags']]
            except:
                pass

            new_mov.genres = genres
            new_mov.themes = themes
            new_mov.tags = tags

            db.session.add(new_mov)
            print(f'adding {i} - {new_mov.name} - {mov["title"]}')

        db.session.commit()
    db.session.close()
