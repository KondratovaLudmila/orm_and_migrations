from sqlalchemy import select
from models import session, db_models

def create_record(model_name: str, values: dict):
    Model = db_models.get(model_name)

    if Model is None:
        raise ValueError("No such model found!")
    
    model = Model(**values)

    session.add(model)
    session.commit()

    
def read_records(model_name: str, values: dict):
    Model = db_models.get(model_name)
    
    if Model is None:
        raise ValueError("No such model found!")
    
    query = select("*").select_from(Model)
    for key, value in values.items():
        query = query.filter(getattr(Model, key)==value)

    records = session.execute(query).all()
    return records

def update_record(model_name: str, values: dict):
    Model = db_models.get(model_name)
    
    if Model is None:
        raise ValueError("No such model found!")
    
    record_id = values.pop("id", None)

    if record_id is None:
        raise ValueError("No id value for update record!")
    
    record = session.query(Model).get(record_id)

    if record is None:
        raise ValueError("No such record to update!")
    
    session.query(Model).filter_by(id=record_id).update(values)
    session.commit()


def remove_record(model_name: str, values: dict):
    Model = db_models.get(model_name)

    if Model is None:
        raise ValueError("No such model found!")
    
    record = session.query(Model).get(values)

    if record is None:
        raise ValueError("No such record to update!")
    
    session.delete(record)
    session.commit()
    
    

    