from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime

from .base import Base


class User(Base):
    __tablename__ = "auth_user"

    email: Mapped[str]
    username: Mapped[str]
    active: Mapped[bool] = mapped_column(server_default="f")
    password: Mapped[Optional[str]]
    login_via_email: Mapped[bool] = mapped_column(server_default="t")
    deleted_at: Mapped[Optional[datetime]]

    role_id: Mapped[UUID] = mapped_column(ForeignKey("role.id"))
    role = relationship("Role", back_populates="users")


class Role(Base):
    __tablename__ = "role"

    name: Mapped[str]
    super_admin: Mapped[bool] = mapped_column(server_default="f")
    required_project_access: Mapped[bool] = mapped_column(server_default="t")
    users = relationship("User", back_populates="role")


class Permission(Base):
    __tablename__ = "permission"

    name: Mapped[str]
    scope: Mapped[str]
    url: Mapped[str]


class RolePermission(Base):
    __tablename__ = "role_permission"

    role_id: Mapped[UUID] = mapped_column(ForeignKey("role.id", ondelete="CASCADE"))
    permission_id: Mapped[UUID] = mapped_column(
        ForeignKey("permission.id", ondelete="CASCADE")
    )

    permissions = relationship("Permission")


class ProductUserAccess(Base):
    __tablename__ = "product_user_access"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("auth_user.id", ondelete="CASCADE")
    )
    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("product.id", ondelete="CASCADE")
    )
    granted: Mapped[bool] = mapped_column(server_default="f")

    user = relationship("User")
    products = relationship("Product", back_populates="accesses")


class UserPasswordReset(Base):
    __tablename__ = "user_reset_password"
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("auth_user.id", ondelete="CASCADE")
    )
    user = relationship("User")
    token_hash: Mapped[str]
    expires_at: Mapped[datetime] = mapped_column(DateTime(True))
