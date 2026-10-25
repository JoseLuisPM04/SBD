import sqlite3
import os

DDL_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS comunidades (
        id_comunidad INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(100) NOT NULL,
        direccion VARCHAR(200) NOT NULL,
        ciudad VARCHAR(100) NOT NULL,
        codigo_postal VARCHAR(10) NOT NULL,
        fecha_creacion DATE NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS viviendas (
        id_vivienda INTEGER PRIMARY KEY AUTOINCREMENT,
        id_comunidad INTEGER NOT NULL,
        numero_unidad VARCHAR(20) NOT NULL,
        planta INTEGER NOT NULL,
        superficie_m2 REAL NOT NULL,
        habitaciones INTEGER NOT NULL,
        FOREIGN KEY (id_comunidad) REFERENCES comunidades(id_comunidad) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS residentes (
        id_residente INTEGER PRIMARY KEY AUTOINCREMENT,
        id_vivienda INTEGER NOT NULL,
        nombre VARCHAR(100) NOT NULL,
        apellidos VARCHAR(100) NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        telefono VARCHAR(20) NOT NULL,
        fecha_ingreso DATE NOT NULL,
        estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVO',
        FOREIGN KEY (id_vivienda) REFERENCES viviendas(id_vivienda) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS perfiles_afinidad (
        id_perfil INTEGER PRIMARY KEY AUTOINCREMENT,
        id_residente INTEGER NOT NULL UNIQUE,
        nivel_sociabilidad INTEGER NOT NULL, -- Escala 1-10
        horario_habitual VARCHAR(50) NOT NULL, -- p.ej. 'Mañana', 'Noche', 'Flexible'
        frecuencia_cocina VARCHAR(50) NOT NULL, -- p.ej. 'Diaria', 'Ocasional', 'Nunca'
        mascotas_aceptadas BOOLEAN NOT NULL,
        intereses VARCHAR(255) NOT NULL,
        FOREIGN KEY (id_residente) REFERENCES residentes(id_residente) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS espacios_comunes (
        id_espacio INTEGER PRIMARY KEY AUTOINCREMENT,
        id_comunidad INTEGER NOT NULL,
        nombre_espacio VARCHAR(100) NOT NULL,
        capacidad_max INTEGER NOT NULL,
        coste_reserva_hora REAL NOT NULL,
        FOREIGN KEY (id_comunidad) REFERENCES comunidades(id_comunidad) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS reservas_espacios (
        id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
        id_espacio INTEGER NOT NULL,
        id_residente INTEGER NOT NULL,
        fecha_reserva DATE NOT NULL,
        hora_inicio VARCHAR(10) NOT NULL,
        hora_fin VARCHAR(10) NOT NULL,
        asistentes_estimados INTEGER NOT NULL,
        FOREIGN KEY (id_espacio) REFERENCES espacios_comunes(id_espacio) ON DELETE CASCADE,
        FOREIGN KEY (id_residente) REFERENCES residentes(id_residente) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS sensores_iot (
        id_sensor INTEGER PRIMARY KEY AUTOINCREMENT,
        id_vivienda INTEGER,
        id_espacio INTEGER,
        tipo_sensor VARCHAR(50) NOT NULL, -- p.ej. 'Electricidad', 'Agua', 'Temperatura'
        ubicacion VARCHAR(100) NOT NULL,
        mac_address VARCHAR(18) UNIQUE NOT NULL,
        FOREIGN KEY (id_vivienda) REFERENCES viviendas(id_vivienda) ON DELETE SET NULL,
        FOREIGN KEY (id_espacio) REFERENCES espacios_comunes(id_espacio) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS lecturas_sensores (
        id_lectura INTEGER PRIMARY KEY AUTOINCREMENT,
        id_sensor INTEGER NOT NULL,
        fecha_hora DATETIME NOT NULL,
        valor_medido REAL NOT NULL,
        unidad_medida VARCHAR(20) NOT NULL,
        FOREIGN KEY (id_sensor) REFERENCES sensores_iot(id_sensor) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS incidencias_convivencia (
        id_incidencia INTEGER PRIMARY KEY AUTOINCREMENT,
        id_comunidad INTEGER NOT NULL,
        id_residente_reporta INTEGER NOT NULL,
        titulo VARCHAR(150) NOT NULL,
        descripcion TEXT NOT NULL,
        prioridad VARCHAR(20) NOT NULL, -- 'Baja', 'Media', 'Alta'
        estado VARCHAR(20) NOT NULL DEFAULT 'Abierta',
        FOREIGN KEY (id_comunidad) REFERENCES comunidades(id_comunidad) ON DELETE CASCADE,
        FOREIGN KEY (id_residente_reporta) REFERENCES residentes(id_residente) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS facturas_gastos_compartidos (
        id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
        id_comunidad INTEGER NOT NULL,
        concepto VARCHAR(150) NOT NULL,
        monto_total REAL NOT NULL,
        fecha_emision DATE NOT NULL,
        fecha_vencimiento DATE NOT NULL,
        estado_pago VARCHAR(20) NOT NULL DEFAULT 'Pendiente',
        FOREIGN KEY (id_comunidad) REFERENCES comunidades(id_comunidad) ON DELETE CASCADE
    );
    """
]

def create_sqlite_database(db_path):
    print(f"Creando base de datos SQLite en: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for statement in DDL_STATEMENTS:
        cursor.execute(statement)
    conn.commit()
    conn.close()
    print("Base de datos creada exitosamente con 10 tablas.")

def create_mysql_database():
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "couser"),
            password=os.getenv("MYSQL_PASSWORD", "copassword"),
            database=os.getenv("MYSQL_DATABASE", "cohousing_db"),
            port=int(os.getenv("MYSQL_PORT", 3306))
        )
        cursor = conn.cursor()
        for stmt in DDL_STATEMENTS:
            mysql_stmt = stmt.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "INT AUTO_INCREMENT PRIMARY KEY")
            cursor.execute(mysql_stmt)
        conn.commit()
        conn.close()
        print("Conexión MySQL realizada y esquema creado.")
    except Exception as e:
        print(f"No se pudo conectar a MySQL Docker (se utilizará la versión SQLite/local): {e}")

def create_postgres_database():
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            user=os.getenv("POSTGRES_USER", "couser"),
            password=os.getenv("POSTGRES_PASSWORD", "copassword"),
            dbname=os.getenv("POSTGRES_DB", "cohousing_db"),
            port=int(os.getenv("POSTGRES_PORT", 5432))
        )
        cursor = conn.cursor()
        for stmt in DDL_STATEMENTS:
            pg_stmt = stmt.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY").replace("DATETIME", "TIMESTAMP")
            cursor.execute(pg_stmt)
        conn.commit()
        conn.close()
        print("Conexión PostgreSQL realizada y esquema creado.")
    except Exception as e:
        print(f"No se pudo conectar a PostgreSQL Docker (se utilizará la versión SQLite/local): {e}")

def create_mariadb_database():
    try: 
        import mysql.connector 
        conn = mysql.connector.connect( 
            host=os.getenv("MARIADB_HOST", "localhost"), 
            user=os.getenv("MARIADB_USER", "couser"), 
            password=os.getenv("MARIADB_PASSWORD", "copassword"), 
            database=os.getenv("MARIADB_DATABASE", "cohousing_db"), 
            port=int(os.getenv("MARIADB_PORT", 3307)),
            collation="utf8mb4_general_ci"
        ) 
        cursor = conn.cursor() 
        for stmt in DDL_STATEMENTS: 
            maria_stmt = stmt.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "INT AUTO_INCREMENT PRIMARY KEY") 
            cursor.execute(maria_stmt) 
        conn.commit() 
        conn.close()
        print("Conexión MariaDB realizada y esquema creado (Puerto 3307).") 
    except Exception as e: 
        print(f"No se pudo conectar a MariaDB Docker: {e}")

if __name__ == "__main__":
    create_sqlite_database("mysql_cohousing.db")
    create_sqlite_database("postgres_cohousing.db")
    create_sqlite_database("mariadb_cohousing.db")

    create_mysql_database()
    create_postgres_database()
    create_mariadb_database()
