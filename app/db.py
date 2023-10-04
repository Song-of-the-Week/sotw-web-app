from sqlalchemy import create_engine
from sqlalchemy import text


def db_tutorial():
    engine = create_engine("postgresql://clarice:password@localhost:5432/sotw")

    with engine.connect() as conn:
        result = conn.execute(text("select 'hello world'"))
        print(result.all())