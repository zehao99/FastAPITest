from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric

from database import Base


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    price = Column(Numeric(10,2))
    forward_pe = Column(Numeric(10,2))
    forward_eps = Column(Numeric(10,2))
    dividend_yeild = Column(Numeric(10,2))
    ma50 = Column(Numeric(10,2))
    ma200 = Column(Numeric(10,2))

    #email = Column(String, unique=True, index=True)
    ##hashed_password = Column(String)
    #is_active = Column(Boolean, default=True)

    # items = relationship("Item", back_populates="owner")
