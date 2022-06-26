from .clean import clean
from .config_file import ConfigFile, ParseError
from .evaluate_ranking import evaluate_ranking
from .get_sentences import get_sentences
from .language import english_name_of_language, is_english, predict_language
from .lemmatize_text import lemmatize_text
from .lemmatize_token import lemmatize_token
from .logger import get_logger
from .match_names import match_names
from .matcher import fast_tokenize, filter_sentences, normalize
from .nlp import nlp
from .parallel_map import parallel_map
from .publication_tei import PublicationTEI
from .unique import unique
