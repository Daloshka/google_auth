Принцип работы авторизации Google
1. Настройка, нужно в панели Google API Console создать Credentials для Web application
Там мы получаем JSON такого типа. 
```
{
  "web": {
    "client_id": "1034431268520-me1n2ug8ntvmu46cnequ1at2h6b9in03.apps.googleusercontent.com",
    "project_id": "daloshka",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "GOCSCX-zK58gYUxbln3N2s3KuCU-rfF-MJA",
    "redirect_uris": [
      "http://localhost:8000/auth/google"
    ]
  }
}
```
❗️Важно указать redirect_uri, где будет происходить генерация токена после перенаправления ответа от Google на ваш Backend.
Типо http://localhost:8000/auth/google

2. Создаём endpoints для авторизации:
/login/google - возвращает ссылку, где пользователь будет проходить авторизацию
/auth/google - сюда пользователь будет автоматически перенаправлен, после того, как пройдёт авторизацию и в ответ должен получить JWT token, который мы сами для него сгенерируем. Потому что уже после авторизации гугла, под капотом мы прочитали данные его аккаунта google и вот что там лежит (код ниже).


```
{
  "id": "107214443299323041424",
  "email": "email@gmail.com",
  "verified_email": true,
  "name": "Daloshka",
  "given_name": "Daloshka",
  "picture": "https://lh3.googleusercontent.com/a/Aag80cJpZL8tqhsd4RyISYWxwniFY3KRXTUZKEPDQVz8qWW5cKFxH0G6=s46-c"
}
```
Эти данные мы обрабатываем через Сental Backend и выдаём JWT token.

