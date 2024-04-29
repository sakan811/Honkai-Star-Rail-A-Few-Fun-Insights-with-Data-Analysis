#    Copyright 2024 Sakan Nirattisaykul
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import os
import sqlite3

from loguru import logger
from pandas import DataFrame
from sqlalchemy import create_engine, Engine, text, Integer, Float, Text
import pandas as pd

logger.add('sqlite_pipeline.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w')


def create_database_and_sqla_engine() -> Engine:
    """
    Creates SQLAlchemy engine and 'hsr' database.
    :return: SQLAlchemy engine
    """
    logger.info('Creating SQLAlchemy Engine...')
    engine = create_engine('sqlite:///hsr.db', echo=True)

    return engine


def add_version(version_dict: dict[float, list[str]]) -> DataFrame:
    """
    Adds version column to DataFrame.
    :param version_dict: Character in each Game Version
    :return: Pandas DataFrame
    """
    logger.info('Adding Version columns...')
    file = 'data/hsr_paths_rarities_elements.xlsx'
    df = pd.read_excel(file)

    df['Version'] = 1.0

    for index, row in df.iterrows():
        character = row['Character']
        for key, value in version_dict.items():
            if character in value:
                df.at[index, 'Version'] = key

    return df


def create_characters_table(df: DataFrame) -> None:
    """
    Creates Characters table.
    :param df: Pandas DataFrame
    :return: None
    """
    logger.info('Creating Characters table...')
    create_database_and_sqla_engine()
    dtype_dict = {
        'Character': 'Text Primary Key',
        'Path': 'Text',
        'Rarity': 'Integer',
        'Element': 'Text',
        'Version': 'Float'
    }
    with sqlite3.connect('hsr.db') as connection:
        df.to_sql('Characters', connection, if_exists='replace', index=False, dtype=dtype_dict)


def create_stats_table() -> None:
    """
    Creates Stats table.
    :return: None
    """
    logger.info('Creating Stats table...')
    directory = 'hsr/hsr_updated'
    create_database_and_sqla_engine()

    df_list = []
    for i, filename in enumerate(os.listdir(directory)):
        if filename.endswith('.xlsx'):
            filepath: str = os.path.join(directory, filename)

            df = pd.read_excel(filepath)

            # Add a new column 'Character' with character name extracted from the filename
            character_name: str = os.path.splitext(filename)[0]  # Extract character name from filename
            df['Character'] = character_name
            df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)

    combined_df['StatID'] = range(0, combined_df.shape[0])
    dtype_dict = {
        'StatID': 'Integer Primary Key',
        'Level': 'Integer',
        'HP': 'Integer',
        'ATK': 'Integer',
        'DEF': 'Integer',
        'Speed': 'Integer',
        'ATK Growth': 'Float',
        'ATK Growth %': 'Float',
        'DEF Growth': 'Float',
        'DEF Growth %': 'Float',
        'HP Growth': 'Float',
        'HP Growth %': 'Float',
        'Speed Growth': 'Float',
        'Speed Growth %': 'Float',
        'Character': 'Text'
    }

    with sqlite3.connect('hsr.db') as connection:
        combined_df.to_sql('Stats', connection, if_exists='replace', index=False, dtype=dtype_dict)


if __name__ == '__main__':
    version_dict = {
        1.1: ['luocha', 'silver-wolf', 'yukong'],
        1.2: ['blade', 'kafka', 'luka'],
        1.3: ['imbibitor-lunae', 'fu-xuan', 'lynx'],
        1.4: ['guinaifen', 'topaz', 'jingliu'],
        1.5: ['argenti', 'hanya', 'huohuo'],
        1.6: ['dr-ratio', 'ruan-mei', 'xueyi'],
        2.0: ['black-swan', 'misha', 'sparkle'],
        2.1: ['acheron', 'aventurine', 'gallagher'],
        2.2: ['robin', 'boothill'],
        2.3: ['jade', 'firefly']
    }
    df = add_version(version_dict)
    create_characters_table(df)
    create_stats_table()
