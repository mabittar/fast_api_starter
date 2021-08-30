
from enum import Enum
from typing import Optional

import pydantic
from pydantic.main import BaseModel
from .common import DateTimeModelMixin, IDModelMixin, Pagination
from pydantic import Field
from pydantic.networks import EmailStr
from pydantic.types import PositiveInt, condecimal
from utils.errors import EmailMustContainsAt, OptionalNumbersError


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"
    not_given = "not_given"

class Point(BaseModel):
    x: float = Field(..., multiple_of=0.01, description="Represents X coordinates",
                     example="1.11", alias="float_numberX")
    y: float = Field(..., multiple_of=0.01, description="Represents Y coordinates",
                     example="3.11", alias="float_numberX")

class PointInDB(IDModelMixin):
    pass 

    class Config:
        title = "Point Model"
        orm_mode = True

        
class ExampleClassRequest(BaseModel):
    """Represents a Resquest to create an Example after POST to Endpoint"""

    name: str = Field(..., max_length=256, description="User name",
                      example="John Lennon", alias="name")
    gender: GenderEnum = Field(...,
                               description="Enumerator Class Model", alias="gender")
    email: EmailStr = Field(alias="email", description="User Email", example="john@beatles.com"
                            )
    float_number: float = Field(
        ..., multiple_of=0.01, description="A float Number", example="1.11", alias="float_number"
    )
    optional_integer: int = Field(
        None, description="An optional positive integer", example="11", alias="optional_integer"
    )
    optional_float: Optional[condecimal(max_digits=18, decimal_places=2)] = Field(
        None, description="An optional float", example="1.12", alias="optional_float"
    )
    
    class Config:
        title = "Exemple Model Creation"
        orm_mode = True
        arbitrary_types_allowed = True

    # @pydantic.root_validator(pre=True)
    # @classmethod
    # def optional_numbers_must_be_null(cls, values):
    #     if ("optional_integer" and "optional_float") not in values:
    #         raise OptionalNumbersError(
    #             title=values["title"], message="Model must have one optional value"
    #         )

    @pydantic.validator('email')
    @classmethod
    def email_must_contains_at(cls, values):
        if "@" not in values:
            raise EmailMustContainsAt(
                title=values["title"], message="Model must have one optional value"
            )


class ExampleInDB(DateTimeModelMixin, IDModelMixin, ExampleClassRequest):
    """Represents an Example Model in Database"""

    public_key: str = Field(..., alias="public key", description="String identification"
                                                   )

    class config:
        orm_model = True
    

class ExamplePaginatedResponse(Pagination, ExampleInDB):
    """Represents a Paginated Example Model to return via API after GET"""
    pass


class ExampleResponse(ExampleInDB):
    """Represents an Example Model to return via API after GET"""
    pass
