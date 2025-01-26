import json
import os.path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from PIL import Image
from flask import Blueprint
from sqlalchemy import func

from constants import MAIN_DIR
from db_loader import db
from sql_models.media_model import Media
from utilities.asset_manager import download_poster
from utilities.devmode_checker import dev_mode

bp = Blueprint('task', __name__)


@bp.route("/sleep_check", methods=['GET'])
def sleep_check():
    print('not sleeping', datetime.now())
    return json.dumps({'ok': True}), 200, {'ContentType': 'application/json'}


@bp.route("/update_banner", methods=['GET'])
def update_banner():
    def make_home_banner():
        def resize_image(img, width, height):
            # Resize the image to the target width and height
            return img.resize((width, height), Image.Resampling.BOX)

        def make_collage(img_array, width, height):
            collage = Image.new("RGB", (width * len(img_array), height))

            with ThreadPoolExecutor() as executor:
                resized_images = list(
                    executor.map(resize_image, img_array, [width] * len(img_array), [height] * len(img_array)))

            for j, img in enumerate(resized_images):
                collage.paste(img, (j * width, 0))

            return collage

        poster_images_path = os.path.join(MAIN_DIR, "static", "posters")
        banner_path = os.path.join(MAIN_DIR, "static", "banners")

        os.makedirs(banner_path, exist_ok=True)

        poster_paths = [os.path.join(poster_images_path, f'{x[0]}_{x[1]}.webp') for x in
                        (db.session.query(Media.id, Media.external_id)
                         .filter(Media.media_type.in_(['movie', 'game', 'manga', 'tv']))
                         .order_by(func.rand())
                         .limit(10)
                         .all())]

        if len(poster_paths) < 1:
            return

        # make collage
        banner = make_collage([Image.open(i) for i in poster_paths], int(500), int(750))
        banner.save(os.path.join(banner_path, 'home_banner.webp'), 'webp', quality=50)


@bp.route("/check_posters", methods=['GET'])
def check_posters():
    poster_dir = os.path.join(MAIN_DIR, 'static', 'posters')
    all_media = db.session.query(Media).all()

    os.makedirs(poster_dir, exist_ok=True)
    poster_ids = {os.path.splitext(x)[0] for x in os.listdir(poster_dir)}

    db_ids = {f'{x.id}_{x.external_id}' for x in all_media}
    db_ids_media = {f'{media.id}_{media.external_id}': media for media in all_media}

    missing_posters = db_ids - poster_ids

    if len(missing_posters) < 1:
        return

    if dev_mode and len(missing_posters) > 100:
        print(len(missing_posters), ' posters missing over local limit, not downloading')
        return

    print(len(missing_posters), ' posters missing, downloading')
    for missing_id in missing_posters:
        matched_media = db_ids_media.get(missing_id)

        if matched_media:
            download_poster(matched_media.poster_path, matched_media.id, matched_media.external_id)

        else:
            print(f"ID {missing_id} not found in database map.")
