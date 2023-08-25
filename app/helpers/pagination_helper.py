from app.schemas.schema_base import PaginationReq


def pagination(pagination_request: PaginationReq, query):
    start_index = (pagination_request.page - 1) * pagination_request.page_size
    query = query.offset(start_index).limit(pagination_request.page_size)
    return query
