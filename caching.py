import functools
import time


response = None
last_request_time = time.time()
def new_request_every(requestor=None, duration=60):
    ''' Modifies a requestor function such that new requests are only made
        every duration. If within duration, serve cached response instead. '''
    
    if requestor is None:
        return functools.partial(new_request_every, duration=duration)
        
    def get_time_since_last_request():
        global last_request_time
        current = time.time()
        elapsed = current - last_request_time
        last_request_time = current
        return elapsed
        
    def get_new_response(*args, **kwargs):
        global response
        new_response = requestor(*args, **kwargs)
        response = new_response
        return response
    
    @functools.wraps(requestor)
    def get_cached_response(*args, **kwargs):
        global response
        if get_time_since_last_request() < duration:
            return response or get_new_response(*args, **kwargs)
        else:
            return get_new_response(*args, **kwargs)

    return get_cached_response
    
token = None
last_token_time = time.time()
def refresh_on_expiration(tokengetter=None, timeout=3600):
    ''' Modifies a tokengetter function such that if the token is still valid,
        it is saved and returned without making another GET request. '''
        
    if tokengetter is None:
        return functools.partial(refresh_on_expiration, timeout=timeout)
    
    def get_token_lifetime():
        global last_token_time
        current = time.time()
        elapsed = current - last_token_time
        last_token_time = current
        return elapsed
    
    def get_new_token(*args, **kwargs):
        global token
        new_token = tokengetter(*args, **kwargs)
        token = new_token
        return token
    
    @functools.wraps(tokengetter)    
    def get_cached_token(*args, **kwargs):
        global token
        if get_token_lifetime() < 3600:
            return token or get_new_token(*args, **kwargs)
        else:
            return get_new_token(*args, **kwargs)
    
    return get_cached_token