import enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    Text,
    ForeignKey
)
from sqlalchemy.orm import (
    relationship
)
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class Roles(enum.Enum):
    any = "Any"
    admin = "Admin"
    manager = "Manager"
    analyst = "Analyst"


class Status(enum.Enum):
    pending = "Pending"
    in_review = "In Review"
    closed = "Closed"


group_tickets = db.Table(
    "group_tickets",
    db.Column("group_id", Integer, ForeignKey("group.id", ondelete="CASCADE")),
    db.Column("ticket_id", Integer, ForeignKey("ticket.id", ondelete="CASCADE"))
)

user_groups = db.Table(
    "user_groups",
    db.Column("group_id", Integer, ForeignKey("group.id", ondelete="CASCADE")),
    db.Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"))
)


class Group(db.Model):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    users = relationship(
        "User",
        secondary="user_groups",
        backref="groups",
        lazy=True,
        passive_deletes=True
    )


class User(db.Model):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(250), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    role = Column(Enum(Roles), default=Roles.any)

    def has_role(self, role: str) -> bool:
        return self.role == role

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)


class Ticket(db.Model):
    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(Status))
    note = Column(Text, nullable=True)

    assigned_groups = relationship("Group", secondary="group_tickets", backref="tickets", lazy=True)
    assigned_users = relationship("User", backref="ticket", lazy=True)
