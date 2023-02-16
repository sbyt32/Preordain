#
# todo: validate the /search/{query} with this.
# from pydantic import validator, BaseModel

# class SearchQuery(str):
#     search: str

#     # def __init__(self, string_literal):
#     #     search = string_literal

#     @validator('search', pre=True)
#     def sanititize_str(cls, v:str):
#         if len(v) >= 50:
#             raise Exception("Hey maybe don't so much")
#         if len(v) <= 0:
#             raise Exception("Maybe like, search for a card")
#         return v