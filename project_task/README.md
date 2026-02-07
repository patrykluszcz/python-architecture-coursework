# E-Commerce Platform Project

## Opis projektu

Projekt realizuje podstawowe funkcjonalności platformy e-commerce implementując moduły do zarządzania **zamówieniami**, **użytkownikami**, **koszykiem** oraz **produktami**.

## Architektura projektu

Projekt jest podzielony na kilka modułów, z których każdy odpowiada za konkretną funkcjonalność:

### Struktura katalogów

```
project_task/
├── src/
│   ├── __init__.py
│   ├── product.py         # Moduł produktów
│   ├── user.py            # Moduł użytkowników
│   ├── cart.py            # Moduł koszyka
│   ├── order.py           # Moduł zamówień
│   ├── ecommerce.py       # Główny moduł platformy
│   └── flask_api.py       # REST API endpoints (Flask)
├── static/
│   ├── css/
│   │   └── style.css      # Style aplikacji
│   └── js/
│       └── app.js         # Logika frontendowa
├── templates/
│   └── index.html         # Strona główna
├── tests/
│   ├── __init__.py
│   ├── test_product.py    # Testy produktów
│   ├── test_user.py       # Testy użytkowników
│   ├── test_cart.py       # Testy koszyka
│   ├── test_order.py      # Testy zamówień
│   └── test_ecommerce.py  # Testy platformy
├── data/                  # Katalog na dane XML
└── README.md
```

## Moduły

### 1. Product (`src/product.py`)

Klasa **`Product`** reprezentuje produkt w systemie.

**Atrybuty:**
- `product_id`: Unikatowy identyfikator produktu
- `name`: Nazwa produktu
- `price`: Cena produktu (musi być > 0)
- `stock`: Dostępna ilość na magazynie (musi być ≥ 0)

**Metody:**
- `decrease_stock(quantity)`: Zmniejsza stan magazynu
- `increase_stock(quantity)`: Zwiększa stan magazynu
- `__repr__()`: Reprezentacja tekstowa

### 2. User (`src/user.py`)

Klasa **`User`** reprezentuje użytkownika platformy.

**Atrybuty:**
- `user_id`: Unikatowy identyfikator użytkownika
- `username`: Nazwa użytkownika
- `email`: Adres email (format: username@domain)
- `address`: Adres dostawy (opcjonalny)

**Metody:**
- `set_address(address)`: Ustawia adres dostawy
- `__repr__()`: Reprezentacja tekstowa

### 3. Cart (`src/cart.py`)

Klasa **`Cart`** reprezentuje koszyk zakupów użytkownika.

**Metody:**
- `add_item(product, quantity)`: Dodaje produkt do koszyka
- `remove_item(product_id)`: Usuwa produkt z koszyka
- `update_quantity(product_id, quantity)`: Zmienia ilość produktu
- `get_items()`: Zwraca listę produktów w koszyku
- `get_total_price()`: Oblicza całkowitą wartość koszyka
- `clear()`: Opróżnia koszyk
- `is_empty()`: Sprawdza czy koszyk jest pusty

### 4. Order (`src/order.py`)

Klasa **`Order`** reprezentuje zamówienie.

**Atrybuty:**
- `order_id`: Unikatowy identyfikator zamówienia
- `user`: Użytkownik, który złożył zamówienie
- `items`: Lista produktów w zamówieniu
- `status`: Status zamówienia (OrderStatus enum)
- `creation_date`: Data utworzenia zamówienia
- `total_price`: Całkowita wartość zamówienia

**Enumeracja `OrderStatus`:**
- `PENDING`: Oczekujące na potwierdzenie
- `CONFIRMED`: Potwierdzone
- `SHIPPED`: Wysłane
- `DELIVERED`: Dostarczone
- `CANCELLED`: Anulowane

**Metody:**
- `update_status(new_status)`: Zmienia status zamówienia
- `to_xml()`: Konwertuje zamówienie do formatu XML
- `__repr__()`: Reprezentacja tekstowa

#### Format XML zamówienia

```xml
<?xml version="1.0" ?>
<order id="ORD-000001">
  <metadata>
    <status>pending</status>
    <creation_date>2026-02-06T15:30:45.123456</creation_date>
    <total_price>2059.97</total_price>
  </metadata>
  <user>
    <id>U001</id>
    <username>john_doe</username>
    <email>john@example.com</email>
    <address>123 Main St</address>
  </user>
  <items>
    <item>
      <product_id>P001</product_id>
      <product_name>Laptop</product_name>
      <unit_price>999.99</unit_price>
      <quantity>2</quantity>
      <item_total>1999.98</item_total>
    </item>
    <item>
      <product_id>P002</product_id>
      <product_name>Mouse</product_name>
      <unit_price>29.99</unit_price>
      <quantity>1</quantity>
      <item_total>29.99</item_total>
    </item>
  </items>
</order>
```

### 5. ECommercePlatform (`src/ecommerce.py`)

## Kodowanie

Projekt jest zgodny ze standardami **PEP-8**:
- Nazwy modułów i zmiennych: `lowercase_with_underscores`
- Nazwy klas: `PascalCase`
- Stałe: `UPPERCASE_WITH_UNDERSCORES`
- Liniowa długość maksymalnie 79 znaków dla kodu

## Testy jednostkowe

Projekt zawiera testy jednostkowe dla wszystkich modułów

### Uruchamianie testów

```bash
# Zainstaluj pytest
python3 -m pip install pytest

# Uruchom wszystkie testy
python3 -m pytest tests/

# Uruchom testy konkretnego modułu
python3 -m pytest tests/test_product.py

# Uruchom z raportowaniem pokrycia
python3 -m pytest tests/ --cov=src
```

### Pokrycie testami

- **test_product.py**: Testy klasy Product (7 testów)
- **test_user.py**: Testy klasy User (6 testów)
- **test_cart.py**: Testy klasy Cart (14 testów)
- **test_order.py**: Testy klasy Order (7 testów)
- **test_ecommerce.py**: Testy platformy (20 testów)

## API REST

## Flask API (`src/flask_api.py`)

Projekt zawiera implementację REST API przy użyciu Flask

### Instalacja zależności

```bash
pip3 install flask
```

### Uruchomienie backendu

```bash
cd project_task

python3 src/flask_api.py
```

API dostępne: `http://127.0.0.1:5004`
Frontend dostępny: `http://127.0.0.1:5004/`

### ⚠️ Ważne: Wybór użytkownika

Przed rozpoczęciem jakichkolwiek operacji (dodawanie produktów do koszyka, tworzenie zamówień itp.) **należy wybrać użytkownika** w interfejsie webowym. Wszystkie operacje wymagają kontekstu zalogowanego użytkownika.

**Endpointy produktów:**
- `GET /api/products` - Lista wszystkich produktów
- `GET /api/products/<product_id>` - Szczegóły produktu
- `POST /api/products` - Dodaj nowy produkt

**Endpointy użytkowników:**
- `GET /api/users` - Lista wszystkich użytkowników
- `GET /api/users/<user_id>` - Szczegóły użytkownika
- `POST /api/users` - Utwórz nowego użytkownika
- `POST /api/users/<user_id>/address` - Zaktualizuj adres użytkownika

**Endpointy koszyka:**
- `GET /api/cart/<user_id>` - Pobierz zawartość koszyka
- `POST /api/cart/<user_id>/add` - Dodaj produkt do koszyka
- `DELETE /api/cart/<user_id>/remove` - Usuń produkt z koszyka

**Endpointy zamówień:**
- `POST /api/orders` - Utwórz zamówienie (checkout)
- `GET /api/orders/<order_id>` - Szczegóły zamówienia
- `PUT /api/orders/<order_id>/status` - Zaktualizuj status zamówienia
- `GET /api/orders/<order_id>/xml` - Pobierz zamówienie w formacie XML
- `GET /api/users/<user_id>/orders` - Lista zamówień użytkownika

## Wymagania

- Python 3.8+
- pytest (do uruchamiania testów)
- flask (do uruchamiania Flask API)

## Funkcjonalności

✅ Zarządzanie produktami (dodawanie, edytowanie stanu magazynu)
✅ Zarządzanie użytkownikami (rejestracja, ustawienie adresu)
✅ Koszyk zakupów (dodawanie, usuwanie, zmiana ilości)
✅ Zamówienia z eksportem do XML
✅ Zarządzanie statusem zamówień
✅ Walidacja danych wejściowych
✅ Testy jednostkowe
✅ Dokumentacja kodu (docstrings)
✅ REST API (Flask)
✅ Zgodność ze standardami PEP-8