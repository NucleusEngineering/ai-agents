# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

def call_function(service, function_name, params):
    try:
        return getattr(service, function_name)(**params)
    except Exception as e:
        print("Cannot invoke the function dynamically. Exception: ")
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
        print("Cannot extract function name from gemini response. Exception: " + e)

def extract_params(response):
    params = {}

    try:
        for part in response.candidates[0].content.parts: 
            for field in part.function_call.args.items():
                params[field[0]] = field[1]
    except AttributeError as e:
        return {}
    except Exception as e:
        print("Cannot extract function parameters name from gemini response. Exception: " + e)

    return params

def extract_text(response):
    try:
        if hasattr(response.candidates[0].content.parts, '__iter__'):
            for part in response.candidates[0].content.parts:
                if part._raw_part.text:
                    return part._raw_part.text
        else:
            return response.candidates[0].content.parts.text    
    except AttributeError as e:
        return ""
    except Exception as e:
        print("Cannot extract text name from gemini response. Exception: " + e)
    
    return ""
    