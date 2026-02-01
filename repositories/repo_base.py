from repositories.db_connect import DBConnect

# Base repository class providing generic CRUD operations
class BaseRepository:
    table_name = None          # required to be set by subclass
    primary_key = "id"         # default
    columns = []               # list of columns in the table
    model_class = None         # corresponding model class

    def __init__(self, db: DBConnect):
        self.db = db

    # ---------------------------
    # CRUD
    # ---------------------------
    def create(self, entity):
        cols = ", ".join(self.columns)
        placeholders = ", ".join(["?"] * len(self.columns))
        values = self.to_row(entity)

        query = f"INSERT INTO {self.table_name} ({cols}) VALUES ({placeholders})"
        new_id = self.db.execute(query, values, commit=True)
        return new_id

    def get(self, id):
        query = f"SELECT * FROM {self.table_name} WHERE {self.primary_key} = ?"
        row = self.db.fetch_one(query, (id,))
        return self.to_entity(row) if row else None

    def update(self, entity):
        set_clause = ", ".join([f"{col} = ?" for col in self.columns])
        values = self.to_row(entity) + [getattr(entity, self.primary_key)]

        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.primary_key} = ?"
        self.db.execute(query, values, commit=True)

    def delete(self, id):
        query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} = ?"
        self.db.execute(query, (id,), commit=True)

    def all(self):
        query = f"SELECT * FROM {self.table_name}"
        rows = self.db.fetch_all(query)
        return [self.to_entity(r) for r in rows]

    # ---------------------------
    # ADVANCED QUERY
    # ---------------------------

    def filter(self, **kwargs):
        if not kwargs:
            return self.all()

        conditions = [f"{k} = ?" for k in kwargs.keys()]
        query = f"SELECT * FROM {self.table_name} WHERE {' AND '.join(conditions)}"
        rows = self.db.fetch_all(query, tuple(kwargs.values()))
        return [self.to_entity(r) for r in rows]

    def exists(self, **kwargs):
        conditions = [f"{k} = ?" for k in kwargs.keys()]
        query = f"SELECT COUNT(*) FROM {self.table_name} WHERE {' AND '.join(conditions)}"
        row = self.db.fetch_one(query, tuple(kwargs.values()))
        return row[0] > 0

    def count_all(self):
        query = f"SELECT COUNT(*) FROM {self.table_name}"
        row = self.db.fetch_one(query)
        return row[0]

    def count_by(self, **kwargs):
        conditions = [f"{k} = ?" for k in kwargs.keys()]
        query = f"SELECT COUNT(*) FROM {self.table_name} WHERE {' AND '.join(conditions)}"
        row = self.db.fetch_one(query, tuple(kwargs.values()))
        return row[0]

    # ---------------------------
    # Conversion helpers
    # ---------------------------
    # Convert a database row to an entity/model instance
    def to_entity(self, row):
        if row is None:
            return None
        return self.model_class(*row)
    
    # Convert an entity/model instance to a list of values for database operations
    def to_row(self, entity):
        return [getattr(entity, col) for col in self.columns]

    # ---------------------------
    # RAW
    # ---------------------------

    def raw(self, query, params=()):
        return self.db.fetch_all(query, params)
