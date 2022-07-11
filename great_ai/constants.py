from .large_file import LargeFileMongo, LargeFileS3
from .persistence.mongodb_driver import MongoDbDriver

ENV_VAR_KEY = "ENVIRONMENT"
PRODUCTION_KEY = "production"
DASHBOARD_PATH = "/dashboard"

MONGO_CONFIG_PATHS = ["mongodb.ini", "mongo.ini", "mongo_db.ini", "mongo-db.ini"]
DEFAULT_TRACING_DATABASE_CONFIG_PATHS = {
    MongoDbDriver: MONGO_CONFIG_PATHS,
}

DEFAULT_LARGE_FILE_CONFIG_PATHS = {
    LargeFileS3: ["s3.ini", "b2.ini"],
    LargeFileMongo: MONGO_CONFIG_PATHS,
}

GITHUB_LINK = "https://github.com/schmelczer/great_ai"

TRAIN_SPLIT_TAG_NAME = "train"
TEST_SPLIT_TAG_NAME = "test"
VALIDATION_SPLIT_TAG_NAME = "validation"
GROUND_TRUTH_TAG_NAME = "ground_truth"
PRODUCTION_TAG_NAME = "production"
DEVELOPMENT_TAG_NAME = "development"
ONLINE_TAG_NAME = "online"

SERVER_NAME = "GreatAI-Server"

SE4ML_WEBSITE = "https://se-ml.github.io/practices"
LIST_ITEM_PREFIX = "  🔩 "
