from sqlalchemy import Column, Integer, TIMESTAMP, text, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.database.database import Base

character_parties = Table(
    "character_parties",
    Base.metadata,
    Column("character_id", Integer, ForeignKey("characters.id", ondelete="CASCADE"), primary_key=True),
    Column("party_id", Integer, ForeignKey("parties.id", ondelete="CASCADE"), primary_key=True),
)


class Characters(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), nullable=False)

    parties = relationship("Parties", secondary="character_parties", back_populates="characters")


class Parties(Base):
    __tablename__ = "parties"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), nullable=False)

    characters = relationship("Characters", secondary="character_parties", back_populates="parties")


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, nullable=False)
    money = Column(Integer, server_default="0", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), nullable=False)
    character_owner_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"),
                                unique=True, nullable=False)