from services import user

def call_function(function_name, params):
    # TODO: hardcoded value for now
    params['user_id'] = 1

    print(params)

    try:
        return getattr(user.User, function_name)(**params)
    except Exception as e:
        print(e)
        return 'Unable to retrieve data from external source'

def extract_function(response):

    try:
        for part in response.candidates[0].content.parts: 
            if part.function_call.name:
                return part.function_call.name
    except AttributeError as e:
        return None
    except Exception as e:
        print(e)

def extract_params(response):
    params = {}

    try:
        for part in response.candidates[0].content.parts: 
            for field in part.function_call.args.items():
                params[field[0]] = field[1]
    except AttributeError as e:
        return {}
    except Exception as e:
        print(e)

    return params

def extract_text(response):
    try:
        for part in response.candidates[0].content.parts: 
            if part.text:
                return part.text
    except Exception as e:
        return ""