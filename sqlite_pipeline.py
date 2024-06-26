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
from sqlite3 import OperationalError

import pandas as pd
import sqlalchemy
from loguru import logger
from pandas import DataFrame
from sqlalchemy import create_engine, text

logger.add('sqlite_pipeline.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w')


class SQLitePipeline:
    def __init__(self, sqlite_database):
        logger.info('Initializing SQLite database...')
        logger.info('If database exist, then connect to database')
        self.database = sqlite_database
        self.engine = create_engine(f'sqlite:///{sqlite_database}')
        self.version_dict = {
            1.1: ['luocha', 'silver-wolf', 'yukong'],
            1.2: ['blade', 'kafka', 'luka'],
            1.3: ['imbibitor-lunae', 'fu-xuan', 'lynx'],
            1.4: ['guinaifen', 'topaz', 'jingliu'],
            1.5: ['argenti', 'hanya', 'huohuo'],
            1.6: ['dr-ratio', 'ruan-mei', 'xueyi'],
            2.0: ['black-swan', 'misha', 'sparkle'],
            2.1: ['acheron', 'aventurine', 'gallagher'],
            2.2: ['robin', 'boothill', 'trailblazer-imaginary'],
            2.3: ['jade', 'firefly'],
            2.4: ['yunli', 'jiaoqiu', 'march-7th-swordmaster']
        }

    def add_version(self, version_and_character_dict: dict[float, list[str]]) -> DataFrame:
        """
        Adds version column to DataFrame.
        :param version_and_character_dict: Character in each Game Version
        :return: Pandas DataFrame
        """
        logger.info('Adding Version columns...')

        file = 'data/hsr_paths_rarities_elements.xlsx'

        dataframe = self._create_dataframe_from_excel(file)

        try:
            logger.info('Iterate over each row in the DataFrame, and add the version corresponding to each character.')
            dataframe['Version'] = dataframe['Character'].apply(
                lambda character: next(
                    (version for version, characters in version_and_character_dict.items() if character in characters),
                    1.0
                )
            )
        except FileNotFoundError as e:
            logger.error(e)
            logger.error(f'{file} not found')
        except Exception as e:
            logger.error(e)
            logger.error('Unexpected error')
        else:
            logger.info('Added Version columns successfully.')
            return dataframe

    def create_characters_table(self, dataframe: DataFrame) -> None:
        """
        Creates Characters table.
        :param dataframe: Pandas DataFrame
        :return: None
        """
        logger.info('Creating Characters table...')
        dtype_dict = {
            'Character': 'Text Primary Key',
            'Path': 'Text',
            'Rarity': 'Integer',
            'Element': 'Text',
            'Version': 'Float'
        }
        try:
            with sqlite3.connect(self.database) as connection:
                dataframe.to_sql('Characters', connection, if_exists='replace', index=False, dtype=dtype_dict)
        except OperationalError as e:
            logger.error(e)
            logger.error(f"{self.database} not found.")
            connection.rollback()
        except ValueError as e:
            logger.error(e)
            logger.error("Data type mismatch.")
            logger.error(f"Check {dtype_dict = }.")
            connection.rollback()
        except Exception as e:
            logger.error(e)
            logger.error('Unexpected error')
            connection.rollback()
        else:
            connection.commit()
            logger.info('Created Characters table successfully.')

    @staticmethod
    def _create_dataframe_from_excel(filepath: str) -> pd.DataFrame:
        """
        Creates DataFrame from Excel file.
        :param filepath: Excel file path
        :return: None
        """
        logger.info('Creating DataFrame from Excel file...')
        try:
            dataframe = pd.read_excel(filepath)
        except pd.errors.ParserError as e:
            logger.error(e)
            logger.error(f'Error parsing Excel file')
        except FileNotFoundError as e:
            logger.error(e)
            logger.error(f'{filepath = } not found')
        except PermissionError as e:
            logger.error(e)
            logger.error(f'{filepath = } : Permission error')
        except ValueError as e:
            logger.error(e)
            logger.error(f'{filepath = } : Not valid Excel file')
        except IOError as e:
            logger.error(e)
            logger.error(f'{filepath = } : File is corrupted')
        except Exception as e:
            logger.error(e)
            logger.error('Error: Unexpected error occurred')
        else:
            logger.info('Created DataFrame successfully.')
            return dataframe

    def read_excel_in_dir(self, directory: str) -> list[pd.DataFrame]:
        """
        Reads Excel files in given directory.
        :param directory: Directory path to Excel files.
        :return: List of DataFrames.
        """
        logger.info('Reading Excel file in the given directory...')
        df_list = []
        try:
            for i, filename in enumerate(os.listdir(directory)):
                logger.debug(f'{filename = }')
                if filename.endswith('.xlsx'):
                    filepath: str = os.path.join(directory, filename)
                    logger.debug(f'{filepath = }')

                    dataframe = self._create_dataframe_from_excel(filepath)

                    logger.info('Add a new column \'Character\' with character name extracted from the filename')
                    character_name: str = os.path.splitext(filename)[0]  # Extract character name from filename
                    dataframe['Character'] = character_name

                    logger.info('Append DataFrame to df_list')
                    df_list.append(dataframe)
        except (FileNotFoundError, PermissionError) as e:
            logger.error(e)
            logger.error(f'Error accessing {directory}')
        else:
            logger.info('Return df_list')
            return df_list

    def create_stats_table(self) -> None:
        """
        Creates Stats table.
        :return: None
        """
        logger.info('Creating Stats table...')
        directory = 'hsr/hsr_updated'

        logger.info(f'Create {directory = } directory if not exist')
        if not os.path.exists(directory):
            os.makedirs(directory)

        df_list = self.read_excel_in_dir(directory)

        combined_df = None
        logger.info('Combine DataFrame from df_list')
        try:
            combined_df = pd.concat(df_list, ignore_index=True)
        except ValueError as e:
            logger.error(e)
            logger.error('No objects to concatenate. df_list is empty')
        except Exception as e:
            logger.error(e)
            logger.error('Unexpected error')
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
            with sqlite3.connect(self.database) as connection:
                combined_df.to_sql('Stats', connection, if_exists='replace', index=False, dtype=dtype_dict)
        except OperationalError as e:
            logger.error(e)
            logger.error(f'{self.database} path is not found.')
            connection.rollback()
        except Exception as e:
            logger.error(e)
            logger.error('Unexpected error')
        else:
            logger.info('Created Stats table successfully')

    def check_level_duplicate(self) -> None:
        """
        Checks whether there is duplicate Level within the same Character.
        :return: None
        """
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            query = """
            SELECT
                Character,
                Level
            FROM (
                SELECT
                    Character,
                    Level,
                    ROW_NUMBER() OVER (PARTITION BY Character, Level ORDER BY Level) AS RowNum
                FROM
                    Stats
            ) subquery
            WHERE
                RowNum > 1;
            """
            cursor.execute(query)

            # Fetch all results
            result = cursor.fetchall()

            if result:
                logger.error(f'Found duplicate Level rows within the same Character in Stats table.')
                logger.error(f'Please re-scrape the Characters\' Stats data.')
                cursor.close()
            else:
                logger.info(f'No duplicate Level rows within the same Character in Stats table.')
                cursor.close()

    def create_views(self) -> None:
        """
        Creates Views.
        :return: None
        """
        logger.info('Creating Views...')

        self._create_character_stats_view()
        self._create_element_character_count_ver()
        self._create_path_character_count_ver()
        self._create_rarity_character_count_ver()

    def _drop_view(self, view_name: str) -> None:
        """
        Drops a SQL view if it exists.
        :param view_name: Name of the view to drop.
        :return: None
        """
        logger.info(f'Dropping {view_name} View if it exists')
        query = f"DROP VIEW IF EXISTS {view_name};"
        try:
            with self.engine.connect() as connection:
                connection.execute(text(query))
        except sqlalchemy.exc.OperationalError as e:
            logger.error(e)
            logger.error(f'{self.database} path is not found.')
        except Exception as e:
            logger.error(f'Error dropping {view_name} View: {e}')
        else:
            logger.info(f'Dropped {view_name} View successfully')

    def _create_character_stats_view(self) -> None:
        """
        Creates CharacterStats View.
        :return: None
        """
        logger.info('Executing create_character_stats_view function...')

        self._drop_view('CharacterStats')

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
            with self.engine.connect() as connection:
                connection.execute(text(query))
        except sqlalchemy.exc.OperationalError as e:
            logger.error(e)
            logger.error(f'{self.database} path is not found.')
        except Exception as e:
            logger.error(f'Error creating CharacterStats View: {e}')
        else:
            logger.info('Created CharacterStats View successfully')

    def _create_element_character_count_ver(self) -> None:
        """
        Creates ElementCharacterCountByVersion View.
        :return: None
        """
        logger.info('Executing create_element_character_count_ver function...')

        self._drop_view('ElementCharacterCountByVersion')

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
            with self.engine.connect() as connection:
                connection.execute(text(query))
        except sqlalchemy.exc.OperationalError as e:
            logger.error(e)
            logger.error(f'{self.database} path is not found.')
        except Exception as e:
            logger.error(f'Error creating ElementCharacterCountByVersion View: {e}')
        else:
            logger.info('Created ElementCharacterCountByVersion View successfully')

    def _create_path_character_count_ver(self) -> None:
        """
        Creates PathCharacterCountByVersion View.
        :return: None
        """
        logger.info('Executing create_path_character_count_ver function...')

        self._drop_view('PathCharacterCountByVersion')

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
            with self.engine.connect() as connection:
                connection.execute(text(query))
        except sqlalchemy.exc.OperationalError as e:
            logger.error(e)
            logger.error(f'{self.database} path is not found.')
        except Exception as e:
            logger.error(f'Error creating PathCharacterCountByVersion View: {e}')
        else:
            logger.info('Created PathCharacterCountByVersion View successfully')

    def _create_rarity_character_count_ver(self) -> None:
        """
        Creates RarityCharacterCountByVersion View.
        :return: None
        """
        logger.info('Executing create_rarity_character_count_ver function...')

        self._drop_view('RarityCharacterCountByVersion')

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
            with self.engine.connect() as connection:
                connection.execute(text(query))
        except sqlalchemy.exc.OperationalError as e:
            logger.error(e)
            logger.error(f'{self.database} path is not found.')
        except Exception as e:
            logger.error(f'Error creating RarityCharacterCountByVersion View: {e}')
        else:
            logger.info('Created RarityCharacterCountByVersion View successfully')


def main() -> None:
    """
    SQLite Pipeline Main function to start the pipeline process.
    :return:
    """
    logger.info('Starting SQLite pipeline process...')

    # Set database name as needed
    database = 'hsr.db'

    sqlite_pipeline = SQLitePipeline(database)
    version_dict = sqlite_pipeline.version_dict

    df = sqlite_pipeline.add_version(version_dict)
    sqlite_pipeline.create_characters_table(df)
    sqlite_pipeline.create_stats_table()
    sqlite_pipeline.create_views()
    sqlite_pipeline.check_level_duplicate()


if __name__ == '__main__':
    main()
