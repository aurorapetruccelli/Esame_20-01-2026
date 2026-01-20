from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artists(min):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select a.id as id, COUNT(*) as c
from album al,artist a
where a.id=al.artist_id
group by a.id
having COUNT(*)>=%s"""
        cursor.execute(query,(min,))
        for row in cursor:
            result.append((row['id'],row["c"]))
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def get_artists_coppie():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct t1.a1 as artista1,t2.a2 as artista2, COUNT(*) as c
from (select distinct a.id as a1,t.genre_id as g1
from album al, artist a, track t
where a.id=al.artist_id and al.id=t.album_id) as t1,
(select distinct a.id as a2,t.genre_id as g2
from album al, artist a, track t
where a.id=al.artist_id and al.id=t.album_id) as t2
where t1.a1<>t2.a2 and t1.g1=t2.g2 
group by t1.a1,t2.a2"""
        cursor.execute(query)
        for row in cursor:
            result.append((row['artista1'],row["artista2"],row["c"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artisti_min_canzoni(durata):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.id as artista
from artist a, album al,track t
where a.id = al.artist_id and al.id=t.album_id 
group by a.id,t.id 
having sum(t.milliseconds)/60000 >= %s"""
        cursor.execute(query,(durata,))
        for row in cursor:
            result.append(row["artista"])
        cursor.close()
        conn.close()
        return result