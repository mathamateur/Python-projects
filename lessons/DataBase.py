import sqlite3


class DataBase:
    con = sqlite3.connect('ch_lessons.sqlite')
    cur = con.cursor()        
    cur.execute('SELECT count(*) '\
                              'AS TOTALNUBEROFTABLES '\
                              'FROM sqlite_sequence')
    
    num_lessons = int(next(cur)[0])

    def get_lesson(self, lesson):
        self.cur.execute(f'SELECT * FROM {lesson} ORDER BY oid ASC')
        return self.cur.fetchall()
