#models.database.py


class Connection:
    __user:str = "Sledge"
    __access:str = "builder"
    

    def conn(self, db:str=None):
        '''Defaults to workers database '''
        if db:
            return f"http://{self.__user}:{self.__access}@localhost:5984/{db}/" 
        else:
            return f"http://{self.__user}:{self.__access}@localhost:5984/cp-workers/"

    @property
    def url(self):
        return self.conn()





 