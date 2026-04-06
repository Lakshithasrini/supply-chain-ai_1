from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/supply_chain_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# Supplier Table
class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    reliability_score = Column(Integer)

# Product Table
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    stock_quantity = Column(Integer)

# Create tables in DB
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Tables created successfully"}
@app.get("/add-data")
def add_data():
    db = SessionLocal()

    supplier1 = Supplier(name="Supplier A", location="Chennai", reliability_score=85)
    supplier2 = Supplier(name="Supplier B", location="Mumbai", reliability_score=70)

    product1 = Product(name="Product X", stock_quantity=100)
    product2 = Product(name="Product Y", stock_quantity=50)

    db.add_all([supplier1, supplier2, product1, product2])
    db.commit()

    return {"message": "Sample data added"}
@app.get("/suppliers")
def get_suppliers():
    db = SessionLocal()
    suppliers = db.query(Supplier).all()
    return suppliers
@app.get("/products")
def get_products():
    db = SessionLocal()
    products = db.query(Product).all()
    return products