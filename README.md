
Architecture
Если бы мы делали "идеальный" Clean Architecture

Твой проект выглядел бы примерно так:

app/

├── domain/
│   ├── entities/
│   ├── exceptions/
│   └── policies/
│
├── application/
│   └── services/
│
├── infrastructure/
│   ├── repositories/
│   ├── database/
│   └── security/
│
├── presentation/
│   ├── api/
│   └── schemas/
│
└── main.py

Но для BookRoom это уже будет скорее усложнение ради архитектуры.

Для учебного проекта или pet-проекта я бы классифицировал твои текущие каталоги так:

Каталог	Слой
api	Presentation
schemas	Presentation
services	Application
models	Domain + Persistence
repositories	Infrastructure
core	Infrastructure
main.py	Composition Root

И, на мой взгляд, для проекта уровня BookRoom это очень удачное разделение. Оно остается понятным, не перегружено абстракциями и при этом уже заметно лучше классического "всё в routers".