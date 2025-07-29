from models import SupportRequest
def create_request(user_id, message):
    req = SupportRequest(user_id=user_id, message=message)
    # TODO: save to database session
    return req
