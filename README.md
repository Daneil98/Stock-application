
STOCK TRADING WEB-APP

A scalable stock trading platform catering to registered users that provides comprehensive information about publicly listed stocks in the US, allows users to make deposits, purchase, sell and trade stocks with leverage seamlessly and securely through the integration of an authenticator for in-app transactions and third-party APIs, namely Tiingo for market data and Braintree for secure payment(deposit) processing. API Endpoints were also created to allow for CRUD operations.

This webapp is live at https://stock-application.onrender.com/


## Run Locally

Clone the project

```bash
  git clone https://github.com/Daneil98/Stock-application
```

Go to the project directory

```bash
  cd Stock-application
```

Install dependencies

```bash
  pip install -r Requirements.txt
```

Prepare migrations

```bash
  python manage.py makemigrations
```

Make migrations

```bash
  python manage.py migrate
```

Start the server

```bash
  python manage.py runserver
```


## Features

- User Authentication: Sign-up, login, and logout functionality with secure password storage.
- Trade: You can buy, sell and trade (short and long) US stocks with leverage easily.
- Stock search and information: Search for the desired US stock and get information on it alongside options to trade.
- Blog: Read articles about the lastest events in the stock market and comment your opinions about the topics.
- Real Time updates: Depending on your Tiingo subscription plan, you can gain access to realtime updates of the US stock market
- In-app Authorization: An otp from Google authenticator is required everytime you want to make a trade, adding another layer of security to the platform.

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

TIINGO_TOKEN = '' 

BRAINTREE_MERCHANT_ID = '' 
BRAINTREE_PUBLIC_KEY = ''   
BRAINTREE_PRIVATE_KEY = ''
BRAINTREE_TOKENIZATION_KEY = ''

CELERY_BROKER_URL = ''
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

NOTE: I used RabbitMQ as my Celery broker
