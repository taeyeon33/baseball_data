class UnitOfWork:
    def __init__(self, connection_factory):
        self.connection_factory = connection_factory
        self.conn = None

    def __enter__(self):
        self.conn = self.connection_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.conn:
                if exc_type is not None:
                    self.conn.rollback()
                else:
                    self.conn.commit()
        
        finally:
            if self.conn:
                self.conn.close()

        return False