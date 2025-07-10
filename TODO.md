# TODO - Django Dan's API Toolkit
#### By: [Daniel Nazarian](https://danielnazarian) 🐧👹

-------------------------------------------------------
## [Unreleased]
----
### Improvements

#### crud library
- make a library for crud operations for django apis
- something to allow each endpoint to just define the model and the viewset


#### validation functions
- validation functions for apis
- things like:
    - validate email
    - validate phone number
    - validate passwords


-----
### 1.2.0



#### get coverage to 100%
- yup



#### pypi test cd script
- upload to test py on each push



#### masked fields shouldn't be removed
- i.e., don't remove the key just put "MASKED" or something?
    - maybe make this an option?
    - by default show the key with no value
    


#### update readme and docs?
- more badges?
- other docs could use clean up
- add docs
    - models?
    - serializers?
    - api response?
    - something to describe the different tools available overall?




##### set custom logger name
- logs show up in sentry and stuff as 'django_dans_api_toolkit'
    - not a huge deal but definitely would be nice to offer an option
    - a bit misleading




#### add lots of tests?
- at least re-evaluate them
- coverage too i guess



### [1.2.0] - 2025-MM-DD
- TODO


---
### 1.1.1


`non_field_errors` is getting shoved into `error_fields`:


```
{'status': 400, 'message': 'Error creating scouting invite.', 'results': None, 'error_fields': {'non_field_errors': [ErrorDetail(string='You have too many pending scouting invites (limit: 5). Please wait for responses before sending more.', code='invalid')]}}
```

something like this should pass

```
        data = {"recipient": str(candidate.id), "message": "Test invite"}
        response = client.post("/api/scouting/invites/", data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "too many pending scouting invites",
            response.data["non_field_errors"][0].lower(),
        )
```


### [1.1.1] - 2025-MM-DD
- TODO


-------------------------------------------------------

##### Copyright 2025 © Daniel Nazarian.
