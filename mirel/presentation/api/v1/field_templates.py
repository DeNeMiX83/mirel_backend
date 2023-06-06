from fastapi import Query


def get_pagination_fields(
    page: int = Query(ge=0, default=0), size: int = Query(ge=1, le=100, default=10)
):
    return page, size