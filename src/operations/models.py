from sqlalchemy import String, Integer, Table, Column, MetaData, TIMESTAMP

metadata = MetaData()

operation = Table('operation',
                  metadata,
                  Column('id', Integer, primary_key=True),
                  Column('quantity', String),
                  Column('figi', String),
                  Column('instrument_type', String, nullable=True),
                  Column('date', TIMESTAMP),
                  Column('type', String),
                  )
