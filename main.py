import sqlite3

conn = sqlite3.connect('db.db')

cursor = conn.cursor()


def init_table():
    cursor.execute("""
    CREATE TABLE products(
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL);
    
    CREATE TABLE customers(
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        first_name TEXT NOT NULL, 
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE);

    CREATE TABLE orders(
        order_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        customer_id INTEGER NOT NULL, 
        product_id INTEGER NOT NULL, 
        quantity INTEGER NOT NULL, 
        order_date DATE NOT NULL, 
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id), 
        FOREIGN KEY(product_id) REFERENCES products(product_id) );
    """)


def init():
    cursor.execute("""
    INSERT INTO products(name, category, price)
    VALUES("IPhone 19 Pro Max", "Phones", 1072);
    INSERT INTO products(name, category, price)
    VALUES("IPhone 17 Ulimate", "Phones", 1272);
    INSERT INTO products(name, category, price)
    VALUES("Roco X10 Life", "Phones", 764.2);
    INSERT INTO products(name, category, price)
    VALUES("Strawberry 3s", "Phones", 543.8);
    INSERT INTO products(name, category, price)
    VALUES("Roco X9 Life", "Phones", 654.2);

    INSERT INTO products(name, category, price)
    VALUES("AppleBook 3s", "Laptop", 1320.5);
    INSERT INTO products(name, category, price)
    VALUES("Samsung 8x9", "Laptop", 1920.32);
    INSERT INTO products(name, category, price)
    VALUES("Samsung 7x9", "Laptop", 1763.7);
    INSERT INTO products(name, category, price)
    VALUES("Asus Nitro 9", "Laptop", 2430.5);
    INSERT INTO products(name, category, price)
    VALUES("Acer Nitro 7", "Laptop", 1824.3);

    INSERT INTO products(name, category, price)
    VALUES("Apple", "Fruit", 2.6);
    INSERT INTO products(name, category, price)
    VALUES("Banana", "Fruit", 3.18);
    INSERT INTO products(name, category, price)
    VALUES("Pear", "Fruit", 1.92);

    INSERT INTO products(name, category, price)
    VALUES("Broccoli", "Vegetable", 1.8);
    INSERT INTO products(name, category, price)
    VALUES("Potato", "Vegetable", 1.2);

    INSERT INTO customers(first_name, last_name, email)
    VALUES("John", "Doe", "johndoe934@gmail.com");
    INSERT INTO customers(first_name, last_name, email)
    VALUES("Agent", "Smith", "agentsmith934@gmail.com");
    INSERT INTO customers(first_name, last_name, email)
    VALUES("Maxim", "Sora", "maximsora2@gmail.com");
    INSERT INTO customers(first_name, last_name, email)
    VALUES("Agent", "003", "agent003@gmail.com");

    INSERT INTO orders(customer_id, product_id, quantity, order_date)
    VALUES(1, 15, 3, "2024-02-03");
    INSERT INTO orders(customer_id, product_id, quantity, order_date) 
    VALUES(1, 11, 1, "2024-02-03");
    INSERT INTO orders(customer_id, product_id, quantity, order_date)
    VALUES(2, 6, 2, "2024-02-04");
    INSERT INTO orders(customer_id, product_id, quantity, order_date)
    VALUES(2, 9, 1, "2024-02-05");
    INSERT INTO orders(customer_id, product_id, quantity, order_date)
    VALUES(3, 3, 1, "2024-03-01");
    INSERT INTO orders(customer_id, product_id, quantity, order_date) 
    VALUES(3, 5, 2, "2024-04-07");
    """)


while True:
    answer = int(input(""" Натисніть:
    1 для додавання продукта
    2 для додавання клієнта
    3 для замовлення товарів
    4 для виведення сумарного обсягу продаж
    5 для виведення кількості замовлень на кожного клієнта
    6 для виведення середнього чеку замовлення
    7 для виведення найбільш популярної категорії
    8 для виведення загальної кількості товарів кожної категорії
    9 для оновлення цін 
    10 для виходу 
    """))
    if answer == 1:
        try:
            name = str(input('name: '))
            category = str(input('category: '))
            price = float(input('price: '))
            cursor.execute(f"""
            INSERT INTO products(name, category, price)
            VALUES("{name}", "{category}", {price});
            """)
            print('Успішно додано!')
        except Exception as error:
            print('Помилка!', str(error))

    elif answer == 2:
        try:
            first_name = str(input('first_name: '))
            last_name = str(input('last_name: '))
            email = str(input('email: '))
            cursor.execute(f"""
            INSERT INTO customers(first_name, last_name, email)
            VALUES("{first_name}", "{last_name}", "{email}");
            """)
            print('Успішно додано!')
        except Exception as error:
            print('Помилка!', str(error))

    elif answer == 3:
        try:
            customer_id = int(input('customer_id: '))
            product_id = int(input('product_id: '))
            quantity = int(input('quantity: '))
            order_date = str(input('order_date: '))
            cursor.execute(f"""
            INSERT INTO orders(customer_id, product_id, quantity, order_date) 
            VALUES({customer_id}, {product_id}, {quantity}, "{order_date}");
            """)
            print('Успішно додано!')
        except Exception as error:
            print('Помилка!', str(error))

    elif answer == 4:
        try:
            print(cursor.execute("""
            SELECT SUM(products.price * orders.quantity) AS total_sales
            FROM orders
            INNER JOIN products ON orders.product_id = products.product_id;
            """).fetchall())
        except Exception as error:
            print('Помилка!', str(error))

    elif answer == 5:
        try:
            print(cursor.execute("""
            SELECT customers.customer_id, customers.first_name, 
                   customers.last_name, SUM(orders.quantity) AS total_quantity
            FROM customers
            INNER JOIN orders ON customers.customer_id = orders.customer_id
            GROUP BY customers.customer_id
            """).fetchall())
        except Exception as error:
            print('Помилка!', str(error))

    elif answer == 6:
        try:
            print(cursor.execute("""
            SELECT AVG(products.price * orders.quantity) AS avg_sales
            FROM orders
            INNER JOIN products ON orders.product_id = products.product_id;
            """).fetchall())
        except Exception as error:
            print('Помилка!', str(error))

    elif answer == 7:
        try:
            print(cursor.execute("""
            SELECT products.product_id, products.category, 
                   COUNT(orders.order_id) AS order_count
            FROM products
            INNER JOIN orders ON products.product_id = orders.product_id
            GROUP BY products.category
            ORDER BY order_count DESC;
            """).fetchall())
        except Exception as error:
            print('Помилка!', str(error))

    elif answer == 8:
        try:
            print(cursor.execute("""
            SELECT products.category, 
                   COUNT(products.product_id) AS products_in_category
            FROM products
            GROUP BY products.category;
            """).fetchall())
        except Exception as error:
            print('Помилка!', str(error))

    elif answer == 9:
        try:
            inflation = 1+int(input('inflation percentage: '))/100
            cursor.execute(f"""
            UPDATE products 
            SET price = price * {inflation}
            WHERE category = 'Phones';
            """)
            print('Успішно змінено!')
        except Exception as error:
            print('Помилка!', str(error))

    elif answer == 10:
        exit()

    else:
        print("Некоректний вибір. Будь ласка, введіть число від 1 до 10.")

    if input("Зберегти зміни? Так-1 Ні-0: ") == 1:
        conn.commit()
        print("Збережено ")

