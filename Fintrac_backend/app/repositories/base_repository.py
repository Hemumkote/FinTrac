from typing import Generic, TypeVar

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

# T is bound to our sqlalchemy model base (use your actual base if we have one)
T = TypeVar("T")
# this allows us to write any functions or classes that work on any type but still keep the type safety


class BaseRepository(Generic[T]):
    """
    Generic base repository that provides a base select query
    with soft-delete filtering.

    Usage:
        class UserRepository(BaseRepository[User]):
            model = User

        # in a method:
        query = self._base_query()  # excludes deleted rows
        query = self._base_query(include_deleted=True)  # includes everything
    """

    model: type[T]  # each subclass sets this

    def __init__(self, session: AsyncSession):
        self.session = session

    def _base_query(self, include_deleted: bool = False) -> Select:
        """Returns a select(model) query, filtering out soft-deleted rows by default."""
        query = select(self.model)
        deleted_at = getattr(self.model, "deleted_at", None)
        if not include_deleted and deleted_at is not None:
            query = query.where(deleted_at.is_(None))
        return query
