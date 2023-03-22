from pydantic import BaseModel, Field


class SchemaCardInfoTableInfo(BaseModel):
    name: str = Field(max_length=255)
    set: str = Field(max_length=12)
    id: str
    uri: str
    tcg_id: str
    tcg_id_etch: str
    groups: list[str]
    new_search: bool = Field(default=True)
    scrape_sales: bool = Field(default=False)
