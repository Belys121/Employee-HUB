# Employee Hub
### Final project SDAcademy
Online aplikace pro správu firemních dat jako komplexní nástroj, který usnadňuje organizaci a sledování všech důležitých informací v rámci společnosti. 
Umožňuje efektivní správu objednávek, což zajišťuje rychlé a přesné zpracování požadavků zákazníků. 
Karta zaměstnance nabízí přehled o pracovních výkonech, dovolené a dalších relevantních údajích, čímž podporuje lepší komunikaci a spolupráci v týmu. 
Díky uživatelsky přívětivému rozhraní a přístupu z jakéhokoli zařízení se zvyšuje produktivita a transparentnost.

Tato aplikace je ideálním řešením pro menší moderní firmy, které chtějí optimalizovat své procesy a zefektivnit správu dat.

## Mockup
- [x] GIT
- [x] creating a wireframe
- [x] design of UI elements
- [x] user scenarios
- [x] mockup presentation
## Basic
- [x] base HTML
- [x] others HTML
- [x] key functions (registration, attaching, searching, order matching...)
- [x] basic testing
## Plná verze
- [x] advanced functions
- [x] performance optimization
- [x] responsive design
- [x] covered by test
- [x] final testing

# Instalations
## Step 1 - Create and activate the virtual environment
    python -m venv venv
    venv\Scripts\activate

## Step 2 - Install package
    pip install -r requirements.txt

## Step 3 - Create migrations
    python manage.py makemigrations

## Step 4 - Migration application
    python manage.py migrate

## Step 5 - Create a superuser
    python manage.py createsuperuser

## Step 6 - Start the development server
    python manage.py runserver

## Voluntary step 7 - Run the tests
    pip install selenium
    python manage.py test/ python manage.py test viewer.tests 


![ER Diagram](ER_diagram_SDA_final_project.png)

