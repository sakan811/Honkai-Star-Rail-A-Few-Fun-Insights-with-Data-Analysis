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

import pandas as pd
from loguru import logger
from pandas import DataFrame
from sqlalchemy import create_engine, Engine, text

logger.add('sqlite_pipeline.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w')


def create_database_and_sqla_engine() -> Engine:
    """
    Creates SQLAlchemy engine and 'hsr' database.
    :return: SQLAlchemy engine
    """
    logger.info('Creating SQLAlchemy Engine...')
    try:
        engine = create_engine('sqlite:///hsr.db', echo=True)
    except Exception as e:
        logger.error(e)
        logger.error('Failed to create SQLAlchemy engine')
    else:
        logger.info('Created SQLAlchemy Engine successfully.')
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

    try:
        for index, row in df.iterrows():
            character = row['Character']
            for key, value in version_dict.items():
                if character in value:
                    df.at[index, 'Version'] = key
    except Exception as e:
        logger.error(e)
        logger.error('Failed to add Version column')
    else:
        logger.info('Added Version columns successfully.')
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
    try:
        with sqlite3.connect('hsr.db') as connection:
            df.to_sql('Characters', connection, if_exists='replace', index=False, dtype=dtype_dict)
    except Exception as e:
        logger.error(e)
        logger.error('Failed to create Characters table')
        connection.rollback()
    else:
        logger.info('Created Characters table successfully.')


def create_stats_table() -> None:
    """
    Creates Stats table.
    :return: None
    """
    logger.info('Creating Stats table...')
    directory = 'hsr/hsr_updated'
    create_database_and_sqla_engine()

    df_list = []

    logger.info('Read Excel file in the given directory')
    try:
        for i, filename in enumerate(os.listdir(directory)):
            logger.debug(f'{filename = }')
            if filename.endswith('.xlsx'):
                filepath: str = os.path.join(directory, filename)
                logger.debug(f'{filepath = }')

                logger.info('Create DataFrame from Excel file')
                df = pd.read_excel(filepath)

                logger.info('Add a new column \'Character\' with character name extracted from the filename')
                character_name: str = os.path.splitext(filename)[0]  # Extract character name from filename
                df['Character'] = character_name

                logger.info('Append DataFrame to df_list')
                df_list.append(df)
    except pd.errors.ParserError as e:
        logger.error(e)
        logger.error(f'Error parsing Excel file')
    except (FileNotFoundError, PermissionError) as e:
        logger.error(e)
        logger.error('Error accessing file or directory')

    combined_df = None
    logger.info('Combine DataFrame from df_list')
    try:
        combined_df = pd.concat(df_list, ignore_index=True)
    except Exception as e:
        logger.error(e)
        logger.error('Failed to concatenate DataFrame')
    else:
        logger.info('Combined DataFrame successfully')

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

    logger.info('Write DataFrame to SQL database table')
    try:
        with sqlite3.connect('hsr.db') as connection:
            combined_df.to_sql('Stats', connection, if_exists='replace', index=False, dtype=dtype_dict)
    except Exception as e:
        logger.error(e)
        logger.error('Failed to create Stats table')
    else:
        logger.info('Created Stats table successfully')


def create_views() -> None:
    """
    Creates Views.
    :return: None
    """
    logger.info('Creating Views...')
    engine = create_database_and_sqla_engine()

    create_character_stats_view(engine)
    create_element_character_count_ver(engine)
    create_path_character_count_ver(engine)
    create_rarity_character_count_ver(engine)


def create_character_stats_view(engine: Engine) -> None:
    """
    Creates CharacterStats View.
    :param engine: SQLAlchemy engine
    :return: None
    """
    logger.info('Executing create_character_stats_view function...')
    logger.info('Drop CharacterStats View if exist')
    query = "DROP VIEW IF EXISTS CharacterStats;"
    try:
        with engine.connect() as connection:
            connection.execute(text(query))
            connection.commit()
    except Exception as e:
        logger.error(f'Error dropping CharacterStats View: {e}')
        connection.rollback()
    else:
        logger.info('Dropped CharacterStats View successfully')

    logger.info('Create CharacterStats View if not exist')
    query = """
    create view CharacterStats as
    select s.Character,
           c.Path,
           c.Rarity,
           c.Element,
           c.Version,
           s.StatID
    from main.Characters c
    left join main.Stats s on s.Character = c.Character
    where StatID is not null;
    """
    try:
        with engine.connect() as connection:
            connection.execute(text(query))
            connection.commit()
    except Exception as e:
        logger.error(f'Error creating CharacterStats View: {e}')
        connection.rollback()
    else:
        logger.info('Created CharacterStats View successfully')


def create_element_character_count_ver(engine: Engine) -> None:
    """
    Creates ElementCharacterCountByVersion View.
    :param engine: SQLAlchemy engine
    :return: None
    """
    logger.info('Executing create_element_character_count_ver function...')
    logger.info('Drop ElementCharacterCountByVersion View if exist')
    query = "DROP VIEW IF EXISTS ElementCharacterCountByVersion;"
    try:
        with engine.connect() as connection:
            connection.execute(text(query))
            connection.commit()
    except Exception as e:
        logger.error(f'Error dropping ElementCharacterCountByVersion View: {e}')
        connection.rollback()
    else:
        logger.info('Dropped ElementCharacterCountByVersion View successfully')

    logger.info('Create ElementCharacterCountByVersion View if not exist')
    query = """
    create view ElementCharacterCountByVersion as
    WITH ElementCounts AS (
    SELECT Version,
           COUNT(DISTINCT CASE WHEN Element = 'Ice' THEN Character END)       AS Ice,
           COUNT(DISTINCT CASE WHEN Element = 'Fire' THEN Character END)      AS Fire,
           COUNT(DISTINCT CASE WHEN Element = 'Lightning' THEN Character END) AS Lightning,
           COUNT(DISTINCT CASE WHEN Element = 'Physical' THEN Character END)  AS Physical,
           COUNT(DISTINCT CASE WHEN Element = 'Wind' THEN Character END)      AS Wind,
           COUNT(DISTINCT CASE WHEN Element = 'Quantum' THEN Character END)   AS Quantum,
           COUNT(DISTINCT CASE WHEN Element = 'Imaginary' THEN Character END) AS Imaginary
    FROM Characters
    GROUP BY Version
    )
    SELECT Version,
            CAST((SELECT SUM(Ice) FROM ElementCounts p WHERE p.Version <= ec.Version) AS INT) AS Ice,
            CAST((SELECT SUM(Fire) FROM ElementCounts p WHERE p.Version <= ec.Version) AS INT) AS Fire,
            CAST((SELECT SUM(Lightning) FROM ElementCounts p WHERE p.Version <= ec.Version) AS INT) AS Lightning,
            CAST((SELECT SUM(Physical) FROM ElementCounts p WHERE p.Version <= ec.Version) AS INT) AS Physical,
            CAST((SELECT SUM(Wind) FROM ElementCounts p WHERE p.Version <= ec.Version) AS INT) AS Wind,
            CAST((SELECT SUM(Quantum) FROM ElementCounts p WHERE p.Version <= ec.Version) AS INT) AS Quantum,
            CAST((SELECT SUM(Imaginary) FROM ElementCounts p WHERE p.Version <= ec.Version) AS INT) AS Imaginary
    FROM ElementCounts ec;
    """
    try:
        with engine.connect() as connection:
            connection.execute(text(query))
            connection.commit()
    except Exception as e:
        logger.error(f'Error creating ElementCharacterCountByVersion View: {e}')
        connection.rollback()
    else:
        logger.info('Created ElementCharacterCountByVersion View successfully')


def create_path_character_count_ver(engine: Engine) -> None:
    """
    Creates PathCharacterCountByVersion View.
    :param engine: SQLAlchemy engine
    :return: None
    """
    logger.info('Executing create_path_character_count_ver function...')
    logger.info('Drop PathCharacterCountByVersion View if exist')
    query = "DROP VIEW IF EXISTS PathCharacterCountByVersion;"
    try:
        with engine.connect() as connection:
            connection.execute(text(query))
            connection.commit()
    except Exception as e:
        logger.error(f'Error dropping PathCharacterCountByVersion View: {e}')
        connection.rollback()
    else:
        logger.info('Dropped PathCharacterCountByVersion View successfully')

    logger.info('Create PathCharacterCountByVersion View if not exist')
    query = """
    create view PathCharacterCountByVersion as
    WITH PathCounts AS (
    SELECT Version,
           COUNT(DISTINCT CASE WHEN Path = 'Abundance' THEN Character END)    AS Abundance,
           COUNT(DISTINCT CASE WHEN Path = 'Erudition' THEN Character END)    AS Erudition,
           COUNT(DISTINCT CASE WHEN Path = 'Hunt' THEN Character END)         AS Hunt,
           COUNT(DISTINCT CASE WHEN Path = 'Destruction' THEN Character END)  AS Destruction,
           COUNT(DISTINCT CASE WHEN Path = 'Preservation' THEN Character END) AS Preservation,
           COUNT(DISTINCT CASE WHEN Path = 'Nihility' THEN Character END)     AS Nihility,
           COUNT(DISTINCT CASE WHEN Path = 'Harmony' THEN Character END)      AS Harmony
           FROM Characters
           GROUP BY Version
    ), PathCountVersion AS (
        SELECT Version,
               (SELECT SUM(Abundance) FROM PathCounts p WHERE p.Version <= pc.Version)    AS Abundance,
               (SELECT SUM(Erudition) FROM PathCounts p WHERE p.Version <= pc.Version)    AS Erudition,
               (SELECT SUM(Hunt) FROM PathCounts p WHERE p.Version <= pc.Version)         AS Hunt,
               (SELECT SUM(Destruction) FROM PathCounts p WHERE p.Version <= pc.Version)  AS Destruction,
               (SELECT SUM(Preservation) FROM PathCounts p WHERE p.Version <= pc.Version) AS Preservation,
               (SELECT SUM(Nihility) FROM PathCounts p WHERE p.Version <= pc.Version)     AS Nihility,
               (SELECT SUM(Harmony) FROM PathCounts p WHERE p.Version <= pc.Version)      AS Harmony
        FROM PathCounts pc
    )
    select pcv.Version,
           cast(pcv.Abundance as int)     AS Abundance,
           cast(pcv.Erudition as int)     AS Erudition,
           cast(pcv.Hunt as int)          AS Hunt,
           cast(pcv.Destruction as int)   AS Destruction,
           cast(pcv.Preservation as int)  AS Preservation,
           cast(pcv.Nihility as int)      AS Nihility,
           cast(pcv.Harmony as int)       AS Harmony
    from PathCountVersion pcv;
    """
    try:
        with engine.connect() as connection:
            connection.execute(text(query))
            connection.commit()
    except Exception as e:
        logger.error(f'Error creating PathCharacterCountByVersion View: {e}')
        connection.rollback()
    else:
        logger.info('Created PathCharacterCountByVersion View successfully')


def create_rarity_character_count_ver(engine: Engine) -> None:
    """
    Creates RarityCharacterCountByVersion View.
    :param engine: SQLAlchemy engine.
    :return: None
    """
    logger.info('Executing create_rarity_character_count_ver function...')
    logger.info('Drop RarityCharacterCountByVersion View if exist')
    query = "DROP VIEW IF EXISTS RarityCharacterCountByVersion;"
    try:
        with engine.connect() as connection:
            connection.execute(text(query))
            connection.commit()
    except Exception as e:
        logger.error(f'Error dropping RarityCharacterCountByVersion View: {e}')
        connection.rollback()
    else:
        logger.info('Dropped RarityCharacterCountByVersion View successfully')

    logger.info('Create RarityCharacterCountByVersion View if not exist')
    query = """
    create view RarityCharacterCountByVersion as
    WITH RarityCounts AS (
        SELECT
            Version,
            COUNT(DISTINCT CASE WHEN Rarity = 5 THEN Character END) AS _5_Star,
            COUNT(DISTINCT CASE WHEN Rarity = 4 THEN Character END) AS _4_Star
        FROM Characters
        GROUP BY Version
    ), RarityCountsVersion AS (
        SELECT
        Version,
        (SELECT SUM(_5_Star) FROM RarityCounts p WHERE p.Version <= rc.Version) AS _5_Star,
        (SELECT SUM(_4_Star) FROM RarityCounts p WHERE p.Version <= rc.Version) AS _4_Star
        FROM RarityCounts rc
    ) 
    select rcv.Version,
           cast(rcv._4_Star as int) AS _4_Star,
           cast(rcv._5_Star as int) AS _5_Star
    from RarityCountsVersion rcv;
    """
    try:
        with engine.connect() as connection:
            connection.execute(text(query))
            connection.commit()
    except Exception as e:
        logger.error(f'Error creating RarityCharacterCountByVersion View: {e}')
        connection.rollback()
    else:
        logger.info('Created RarityCharacterCountByVersion View successfully')


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
    create_views()
