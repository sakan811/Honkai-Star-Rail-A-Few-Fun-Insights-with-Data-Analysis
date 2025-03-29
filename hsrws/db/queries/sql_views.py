"""SQL queries for database views."""


def get_rarity_char_count_by_ver() -> str:
    """
    Gets 'rarity character count by version' query.

    Returns:
        SQL query string.
    """
    query = """
        create view RarityCharacterCountByVersion as
        WITH RarityCounts AS (
            SELECT
                Version,
                COUNT(DISTINCT CASE WHEN Rarity = '5-Star' THEN Character END) AS _5_Star,
                COUNT(DISTINCT CASE WHEN Rarity = '4-Star' THEN Character END) AS _4_Star
            FROM HsrCharacters
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
    return query


def get_path_char_count_by_ver() -> str:
    """
    Gets 'path character count by version' query.

    Returns:
        SQL query string.
    """
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
                FROM HsrCharacters
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
    return query


def get_element_char_count_by_ver() -> str:
    """
    Gets 'Element Character Count by Version' query.

    Returns:
        SQL query string.
    """
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
        FROM HsrCharacters
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
    return query
