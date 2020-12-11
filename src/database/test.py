import pandas as pd
from repository import insert
from base import Base, engine

Base.metadata.create_all(engine)
df = pd.read_csv('cleaned_for_db.csv')
df = df.drop('land_surface', inplace=True, axis=1)
insert(df)