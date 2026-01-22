from sqlalchemy.orm.query import Query


def paginate_query(query: Query, page: int, page_size: int = 5) -> tuple[list, bool]:
    offset = page_size * (page - 1)
    entities = query.offset(offset).limit(page_size + 1).all()
    has_next_page = len(entities) == page_size + 1

    return (entities[:page_size], has_next_page)
