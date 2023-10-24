import os

from sqlalchemy import case

from sql_models.media_model import CardTemplate

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
HASH_SIZE = 14

# noinspection PyTypeChecker
CARD_TYPE_PRIORITY = case(
    (CardTemplate.type == 'Normal Monster', 1),
    (CardTemplate.type == 'Effect Monster', 2),
    (CardTemplate.type == 'Flip Effect Monster', 3),
    (CardTemplate.type == 'Union Effect Monster', 4),
    (CardTemplate.type == 'Tuner Monster', 5),
    (CardTemplate.type == 'Gemini Monster', 6),
    (CardTemplate.type == 'Normal Tuner Monster', 7),
    (CardTemplate.type == 'Spirit Monster', 8),
    (CardTemplate.type == 'Normal Tuner Monster', 10),
    (CardTemplate.type == 'Toon Monster', 11),
    (CardTemplate.type == 'Pendulum Normal Monster', 12),
    (CardTemplate.type == 'Pendulum Effect Monster', 13),
    (CardTemplate.type == 'Pendulum Flip Effect Monster', 14),
    (CardTemplate.type == 'Pendulum Tuner Effect Monster', 15),
    (CardTemplate.type == 'Pendulum Effect Ritual Monster', 16),
    (CardTemplate.type == 'Synchro Pendulum Effect Monster', 17),
    (CardTemplate.type == 'XYZ Pendulum Effect Monster', 18),
    (CardTemplate.type == 'Fusion Monster', 19),
    (CardTemplate.type == 'Ritual Monster', 20),
    (CardTemplate.type == 'Synchro Monster', 21),
    (CardTemplate.type == 'Synchro Tuner Monster', 22),
    (CardTemplate.type == 'XYZ Monster', 23),
    (CardTemplate.type == 'Link Monster', 24),
    (CardTemplate.type == 'Spell Card', 25),
    (CardTemplate.type == 'Trap Card', 26),
    (CardTemplate.type == 'Token', 27),
)
