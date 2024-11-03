import sqlalchemy as sa
from tinydb import TinyDB, Query
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Date, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# Create a base class for declarative models
Base = declarative_base()

# Define the FishingReport model
class FishingReport(Base):
    __tablename__ = 'fishing_reports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    angler = Column(String, nullable=False, key='Angler')
    date = Column(String, nullable=False, key='Date')
    day = Column(Integer, nullable=False, key='Day')
    month = Column(String, nullable=False, key='Month')
    year = Column(Integer, nullable=False, key='Year')
    area = Column(String, nullable=False, key='Area')
    beat = Column(String, nullable=False, key='Beat')
    fishing = Column(String, nullable=False, key='Fishing')
    no_of_anglers = Column(String, nullable=False, key='No. of Anglers')
    fishing_report_id = Column(String, nullable=False, unique=True, key='__ID')  # Using string for consistency with your JSON
    comment = Column(Text, nullable=True, key='Comment')
    barbel_count = Column(Integer, nullable=True, key='# Barbel')
    chub_count = Column(Integer, nullable=True, key='# Chub')
    pike_count = Column(Integer, nullable=True, key='# Pike')
    trout_count = Column(Integer, nullable=True, key='# Trout')
    grayling_count = Column(Integer, nullable=True, key='# Grayling')
    other_count = Column(Integer, nullable=True, key='# Other')
    page_url = Column(String, nullable=True, key='Page URL')


# Create an SQLite database and a session
engine = create_engine('sqlite:///fishing_reports.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Load both datasets
db = TinyDB('db2.json')

# Prepare to check for duplicates using the __ID field
Data = Query()


# get all datasets
all_datasets = db.all()

# Insert all datasets into the database
for dataset in all_datasets:
    # Create a new FishingReport object
    new_report = FishingReport(
        angler=dataset['Angler'],
        date=dataset['Date'],
        day=dataset['Day'],
        month=dataset['Month'],
        year=dataset['Year'],
        area=dataset['Area'],
        beat=dataset['Beat'],
        fishing=dataset['Fishing'],
        no_of_anglers=dataset['No. of Anglers'],
        fishing_report_id=dataset['__ID'],
        comment=dataset['Comment'],
        barbel_count=dataset.get('# Barbel', None),
        chub_count=dataset.get('# Chub', None),
        pike_count=dataset.get('# Pike', None),
        trout_count=dataset.get('# Trout', None),
        grayling_count=dataset.get('# Grayling', None),
        other_count=dataset.get('# Other', None),
        page_url=dataset['Page URL']
    )
    
    # Attempt to add and commit the new report
    try:
        session.add(new_report)
        session.commit()
        print(f"Inserted new dataset for __ID: {dataset['__ID']}")
    except IntegrityError:
        session.rollback()  # Rollback the session if there's an error
        print(f"Data already exists for __ID: {dataset['__ID']}")


# Close the session
session.close()

print("Database created and sample data inserted.")
