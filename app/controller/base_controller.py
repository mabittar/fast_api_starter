from typing import List, Union

from sqlalchemy.orm.query import Query
from sqlalchemy.sql.operators import asc_op, desc_op
from sqlalchemy.sql.schema import Column
from orm.base_orm import BaseORM
from pydantic import BaseModel


class BaseController(BaseORM):
    def __init__(self, model: BaseModel):
        BaseORM.__init__(self)
        self.model = model

    def add(self, data: Union[BaseModel, List[BaseModel]]) -> None:
        if not isinstance(data, list):
            data = [data]
        self.session.add_all(data)

    def delete(self, data: BaseModel) -> None:
        self.session.delete(data)

    def new_query(self) -> Query:
        return self.session.query(self.model)

    def lock(self, query: Query) -> Query:
        return query.with_for_update(of=self.model)

    def get_first(self, query: Query) -> BaseModel:
        return query.first()

    def get_all(self, query: Query) -> List[BaseModel]:
        return query.all()

    @staticmethod
    def __asc(query: Query, column: Column) -> Query:
        new_query = query.order_by(asc_op(column))
        return new_query

    @staticmethod
    def __desc(query: Query, column: Column) -> Query:
        new_query = query.order_by(desc_op(column))
        return new_query

    @staticmethod
    def _order_by(query: Query, column: Column, order: str) -> Query:
        method = {
            "asc": BaseORM.__asc,
            "desc": BaseORM.__desc,
        }
        return method[order](query, column)