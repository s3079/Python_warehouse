class Config:

    DB_HOST = "localhost"
    DB_NAME = "warehouse"
    DB_USER = "root"
    DB_PASSWORD = "LeeNghien97@"

    WINDOW_SIZE = "1200x800"
    
    @classmethod
    def get_db_config(cls):
        return {
            "host": cls.DB_HOST,
            "database": cls.DB_NAME,
            "user": cls.DB_USER,
            "password": cls.DB_PASSWORD
        }
