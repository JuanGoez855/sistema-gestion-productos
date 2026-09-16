from pydantic import BaseModel, Field, field_validator


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=500)
    price: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    category_id: int

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError(
                "El nombre del producto no puede estar vacío"
            )

        return value


class ProductUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )
    description: str | None = Field(
        default=None,
        max_length=500
    )
    price: float | None = Field(
        default=None,
        gt=0
    )
    stock: int | None = Field(
        default=None,
        ge=0
    )
    category_id: int | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None):
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError(
                "El nombre del producto no puede estar vacío"
            )

        return value


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    stock: int
    category_id: int
    created_by_id: int

    model_config = {
        "from_attributes": True
    }