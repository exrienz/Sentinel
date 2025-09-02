from typing import Annotated

from fastapi import Header
from sqlalchemy import String, cast, literal, select
from sqlalchemy.orm import selectinload

from src.application.middlewares.user_context import (
    current_user_id_var,
    current_user_var,
)
from src.application.schemas.auth import TokenDataSchema
from src.domain.entity import Product, Token
from src.domain.entity.project_management import Environment
from src.domain.entity.user_access import Role, User
from src.infrastructure.database.config import AsyncSessionFactory


class SetContextUser:
    async def __call__(
        self,
        x_token: Annotated[str | None, Header()] = None,
    ):
        if x_token is None:
            return

        async with AsyncSessionFactory() as session:
            api_stmt = select(literal("all").label("result")).where(
                Token.token == x_token
            )

            product_stmt = select(cast(Product.id.label("result"), String)).where(
                Product.apiKey == x_token
            )

            stmt = product_stmt.union(api_stmt).limit(1)
            query = await session.execute(stmt)
            res = query.scalar_one_or_none()

            if res is None:
                return

            user_stmt = (
                select(User)
                .join(Role)
                .options(selectinload(User.role))
                .where(Role.name == "Service", User.active)
                .limit(1)
            )
            query = await session.execute(user_stmt)
            user = query.scalar_one_or_none()
            if user is None:
                return

            project_id = "all"
            if res != "all":
                stmt = (
                    select(Environment.project_id)
                    .join(Product)
                    .where(Product.id == res)
                )
                proj_query = await session.execute(stmt)
                project_id = proj_query.scalar_one_or_none()

        token_data = TokenDataSchema(
            userid=str(user.id),
            role=user.role.name,
            is_admin=False,
            high_privilege=False,
            role_id=str(user.role.id),
            required_project_access=True,
            username=user.username,
        )

        current_user_id_var.set(user.id)

        user_data = {
            **token_data.model_dump(),
            "service_account": True,
            "service_product_id": res,
            "service_project_id": project_id,
        }
        current_user_var.set(user_data)
