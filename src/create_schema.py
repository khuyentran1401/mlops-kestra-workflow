from pandera import Column, DataFrameSchema
from pandera.dtypes import DateTime

raw_schema = DataFrameSchema({"pickup_datetime": Column(DateTime)})
