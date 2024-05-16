# link-shortener
Simple link shortener project

## Start the development server

Install all required packages:
> `pip install -r requirements.txt`

Perform required migrations - navigate into dir with `manage.py` file and run:
> `python3 manage.py runmigrations`

To start the development server:
> `python3 manage.py runserver`


## Run the tests
Navigate into dir with `pytest.ini` file and run the command:
> `pytest ./links_handling/*`


## API Description

### Endpoint for shortening the links
POST `localhost:8000/create-short-url`

Payload:
```
{
    "original_url": "<url-to-shorten>"
}
```


Response HTTP 201 Created
```
{
    "original_url": "<url-to-shorten>",
    "short_url": "<shorted-url>"
}

```

Example Payload:
```
{
    "original_url": "https://example.com/test-1/23123"
}

```

Example Response:
```
{
    "original_url": "https://example.com/test-1/23123",
    "short_url": "http://localhost:8000/UKS1k4"
}

```


### Endpoint for getting original link from the shortened link
GET localhost:8000/<short-url-code>

Response - HTTP 200 OK
```
{
    "original_url": "<original-url>"
}

```

Example request:
GET `http://localhost:8000/UKS1k4`


Example response:
```
{
    "original_url":"https://example.com/test-1/23123"
}
```




