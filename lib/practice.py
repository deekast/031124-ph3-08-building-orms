from . import CONN
from . import CURSOR

class Movie:
    def __init__(self, title:str, year:int, id:int=None):
        self.title = title
        self.year = year
        self.id = id

    def __repr__(self):
        return f'Movie(id={self.id}, title={self.title}, year={self.year})'


    # --- SQL CLASS METHODS --- #

    @classmethod
    def create_table(cls):
        sql = '''CREAT TABLE IF NOT EXISTS movies ( 
            id INTEGER PRIMARY KEY,
            title TEXT, 
            year INTEGER 
        )'''

        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def get_all(cls):
        sql= ''' SELECT * FROM movies'''

        read_all_tuples = CURSOR.execute(sql).fetchall()
    
        all_movies = []

        for tup in read_all_tuples:
            movie = Movie(title=tup[1], id=tup[0])
            all_movies.append(movie)

        return all_movies

    @classmethod
    def get_by_id(cls, id:int):
        sql='''SELECT * FROM courses WHERE id = ?'''

        found_movie_tuple = CURSOR.execute(sql, [ id ]).fetchone()

        if found_movie_tuple:
            return Movie(name=found_movie_tuple[1], id=found_movie_tuple[0])

    # --- SQL INSTANCE METHODS --- #

    def create(self):
       sql = '''INSERT INTO courses ( name )
       VALUES ( ?  )
       '''

       CURSOR.execute(sql, [self.title, self.year, self.id])
       CONN.commit()

       last_row_sql = 'SELECT * FROM movies ORDER by ID DESC LIMIT 1'
       last_row_tuple = CURSOR.execute(last_row_sql).fetchone()

    def update(self):
        sql = '''UPDATE movies SET name = ?
        WHERE id = ?
        '''

        CURSOR.execute(sql, [self.title,self.year, self.id])


    def save(self):
        
        if not self.id:
            self.create()
        else:
            self.update()

    
    def destroy(self):
        sql = '''SELECT * FROM students WHERE movie_id = ?'''

        movie_tuples = CURSOR.execute(sql, [self.id]).fetchall()

        return [
            Movie(id=movie_tuple[0], title=movie_tuple[1], year=movie_tuple[2])
            for movie_tuple in movie_tuples
        ]