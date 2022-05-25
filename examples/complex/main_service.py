from great_ai import configure, create_service

configure(development_mode_override=True)

from predict_domain import predict_domain

app = create_service(predict_domain)
