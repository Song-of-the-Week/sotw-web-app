from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import Session

def db_tutorial():
    engine = create_engine("postgresql://clarice:password@localhost:5432/sotw")

    with Session(engine) as session:
        result = session.execute(text("select 'hello world'"))
        print(result.all())