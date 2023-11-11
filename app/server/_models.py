from sqlalchemy import Table, Column
from sqlalchemy.orm import registry as registry_class

from app.base.database.models import id_columns, timed_columns


def load_models(registry: registry_class):
    server = Table(
        'servers',
        registry.metadata,
        *id_columns(),
        *timed_columns(),
    )
