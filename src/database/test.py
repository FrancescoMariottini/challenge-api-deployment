import pandas as pd
from repository import insert
from base import Base, engine

Base.metadata.create_all(engine)
df = pd.read_csv(r'C:\Users\opaps\source\BeCode\Project API-Docker\challenge-api-deployment\src\database\cleaned_for_db.csv')
insert(df)