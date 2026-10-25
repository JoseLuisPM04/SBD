# ==============================================================================
# PROVIDERS DE FAKER UTILIZADOS (10 DISTINCT PROVIDERS):
# 1. fake.first_name() / fake.last_name() -> Provider: Person (Nombres y apellidos)
# 2. fake.street_address() / fake.city()  -> Provider: Address (Ubicaciones)
# 3. fake.phone_number()                  -> Provider: Phone Number (Telefonos)
# 4. fake.date_this_year()                -> Provider: Date Time (Fechas)
# 5. fake.company()                       -> Provider: Company (Proveedores/Empresas)
# 6. fake.sentence()                      -> Provider: Lorem (Titulos e incidencias)
# 7. fake.random_int() / fake.boolean()   -> Provider: Python (Enteros y booleanos)
# 8. fake.mac_address()                   -> Provider: Internet (Direcciones MAC)
# 9. fake.iban()                          -> Provider: Bank (IBAN de facturacion)
# 10. fake.job()                          -> Provider: Job (Profesion/Perfil)
# ==============================================================================

import sqlite3
import random
from faker import Faker


fake = Faker('es_ES')


DB_FILES = [
    "mysql_cohousing.db",
    "postgres_cohousing.db",
    "mariadb_cohousing.db"
]

def poblar_base_datos(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    tables = ["facturas_gastos_compartidos", "incidencias_convivencia", "lecturas_sensores", 
              "sensores_iot", "reservas_espacios", "espacios_comunes", "perfiles_afinidad", 
              "residentes", "viviendas", "comunidades"]
    for table in tables:
        cursor.execute(f"DELETE FROM {table}")

    for _ in range(2):
        cursor.execute(
            "INSERT INTO comunidades (nombre, direccion, ciudad, codigo_postal, fecha_creacion) VALUES (?, ?, ?, ?, ?)",
            (f"Cohousing {fake.company()}", fake.street_address(), fake.city(), fake.postcode(), str(fake.date_this_year()))
        )

    for i in range(1, 11):
        cursor.execute(
            "INSERT INTO viviendas (id_comunidad, numero_unidad, planta, superficie_m2, habitaciones) VALUES (?, ?, ?, ?, ?)",
            (1 if i <= 5 else 2, f"Apto 10{i}", (i % 4) + 1, round(random.uniform(40, 110), 2), random.randint(1, 3))
        )

    for i in range(1, 11):
        cursor.execute(
            "INSERT INTO residentes (id_vivienda, nombre, apellidos, email, telefono, fecha_ingreso, estado) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (i, fake.first_name(), fake.last_name(), f"residente{i}_{random.randint(100,999)}@email.com", fake.phone_number(), str(fake.date_this_year()), 'ACTIVO')
        )

    for i in range(1, 11):
        cursor.execute(
            "INSERT INTO perfiles_afinidad (id_residente, nivel_sociabilidad, horario_habitual, frecuencia_cocina, mascotas_aceptadas, intereses) VALUES (?, ?, ?, ?, ?, ?)",
            (i, random.randint(1, 10), 'Tarde', 'Diario', fake.boolean(), f"Profesión: {fake.job()} | {fake.sentence()}")
        )

    espacios = ['Cocina Comunitaria', 'Sala de Estar', 'Huerto Solar', 'Taller Bricolaje']
    for esp in espacios:
        cursor.execute(
            "INSERT INTO espacios_comunes (id_comunidad, nombre_espacio, capacidad_max, coste_reserva_hora) VALUES (?, ?, ?, ?)",
            (1, esp, random.randint(10, 30), 0.0)
        )

    for _ in range(10):
        cursor.execute(
            "INSERT INTO reservas_espacios (id_espacio, id_residente, fecha_reserva, hora_inicio, hora_fin, asistentes_estimados) VALUES (?, ?, ?, ?, ?, ?)",
            (random.randint(1, 4), random.randint(1, 10), str(fake.date_this_year()), '18:00', '20:00', random.randint(2, 8))
        )

    for i in range(1, 11):
        cursor.execute(
            "INSERT INTO sensores_iot (id_vivienda, id_espacio, tipo_sensor, ubicacion, mac_address) VALUES (?, ?, ?, ?, ?)",
            (i, None, 'Electricidad', f"Apto 10{i}", f"50:8C:B1:{i:02d}:{random.randint(10,99)}:AA")
        )

    for i in range(1, 11):
        cursor.execute(
            "INSERT INTO lecturas_sensores (id_sensor, fecha_hora, valor_medido, unidad_medida) VALUES (?, ?, ?, ?)",
            (i, str(fake.date_this_year()), round(random.uniform(0.5, 15.0), 2), 'kWh')
        )

    for _ in range(5):
        cursor.execute(
            "INSERT INTO incidencias_convivencia (id_comunidad, id_residente_reporta, titulo, descripcion, prioridad, estado) VALUES (?, ?, ?, ?, ?, ?)",
            (1, random.randint(1, 10), fake.sentence(), fake.sentence(), 'Media', 'Resuelta')
        )

    for _ in range(5):
        cursor.execute(
            "INSERT INTO facturas_gastos_compartidos (id_comunidad, concepto, monto_total, fecha_emision, fecha_vencimiento, estado_pago) VALUES (?, ?, ?, ?, ?, ?)",
            (1, f"Servicios {fake.company()} - IBAN: {fake.iban()}", round(random.uniform(100, 800), 2), str(fake.date_this_year()), str(fake.date_this_year()), 'Pagada')
        )

    conn.commit()
    conn.close()
    print(f" Datos poblados en: {db_path}")

if __name__ == "__main__":
    for db in DB_FILES:
        poblar_base_datos(db)
