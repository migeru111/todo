import psycopg2
from psycopg2.extras import RealDictCursor
from abc import ABC,abstractmethod

class AccessorIF(ABC):
    @abstractmethod
    def fetch_all(self):
        pass

    @abstractmethod
    def fetch_by_id(self):
        pass

    @abstractmethod
    def update(self,user_id):
        pass

    @abstractmethod
    def delete(self,user_id):
        pass

    @abstractmethod
    def create(self):
        pass

class DbAccessor(AccessorIF):
    def __init__(self):
        
        self.connect=psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password="pass",
            port=5432,
            cursor_factory=RealDictCursor
        )
        self.cur=self.connect.cursor()

    def fetch_all(self):
        self.cur.execute("SELECT userid,content FROM todos;")
        # resがpsycopg2.extras.RealDictRow型なのでdict変換
        res=self.cur.fetchall()
        res= [dict(i) for i in res]
        return res

    def fetch_by_id(self, user_id):
        print(f"user_id,{user_id}")
        self.cur.execute("SELECT * FROM todos WHERE userId = %s;",(user_id,))
        return self.cur.fetchall()

    def create(self,content):
        self.cur.execute("insert into todos (contents) values (%s) RETURNING userId;",(content,))
        self.connect.commit()

        res=self.cur.fetchone()
        # resがpsycopg2.extras.RealDictRow型なのでdict変換
        return dict(res)

    def delete(self,user_id):
        self.cur.execute(f"delete from todos where user_id = f{user_id};")
        self.connect.commit()
        

    def update(self,user_id,content):
        self.cur.execute("update todos set contents = %s where userid = %s RETURNING userId;",(content,user_id))
        self.connect.commit()

        return self.cur.fetchone()
