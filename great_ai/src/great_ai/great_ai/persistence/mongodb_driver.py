from .tracing_database_driver import TracingDatabaseDriver


class MongoDbDriver(TracingDatabaseDriver):
    is_production_ready = True
