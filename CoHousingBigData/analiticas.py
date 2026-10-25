import sqlite3
import json

def export_mysql_analytics(db_path, output_json):
    """
    CONSULTA 1 (MySQL): Correlación de Perfiles de Afinidad y Uso de Espacios Comunes.
    Une: residentes JOIN perfiles_afinidad JOIN reservas_espacios JOIN espacios_comunes.
    IMPORTANCIA: Permite evaluar cómo influyen las preferencias sociales y hábitos
    del residente en el uso real de las áreas comunes, ayudando a optimizar horarios.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    SELECT 
        r.nombre || ' ' || r.apellidos AS residente,
        p.nivel_sociabilidad,
        p.horario_habitual,
        p.intereses,
        e.nombre_espacio,
        COUNT(res.id_reserva) AS total_reservas,
        SUM(res.asistentes_estimados) AS total_asistentes_acumulados
    FROM residentes r
    JOIN perfiles_afinidad p ON r.id_residente = p.id_residente
    JOIN reservas_espacios res ON r.id_residente = res.id_residente
    JOIN espacios_comunes e ON res.id_espacio = e.id_espacio
    GROUP BY r.id_residente, e.id_espacio
    ORDER BY total_reservas DESC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    
    data = {
        "origen_base_datos": "MySQL (cohousing_db)",
        "analisis": "Correlación entre Perfil Sociológico y Uso de Instalaciones Comunes",
        "justificacion_importancia": "Unir estas 4 tablas es crítico para la junta del cohousing, ya que revela si las salas diseñadas responden a la sociabilidad e intereses reales de los vecinos. Evita inversiones en zonas comunitarias infrautilizadas y fomenta actividades grupales afines.",
        "indicadores_clave": []
    }
    
    for row in rows:
        data["indicadores_clave"].append({
            "residente": row[0],
            "nivel_sociabilidad": row[1],
            "horario_preferido": row[2],
            "intereses": row[3],
            "espacio_comun_reservado": row[4],
            "total_reservas_realizadas": row[5],
            "asistentes_totales_convocados": row[6]
        })
        
    conn.close()
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Exportado informe JSON de MySQL a: {output_json}")

def export_postgres_analytics(db_path, output_json):
    """
    CONSULTA 2 (PostgreSQL): Eficiencia Energética e IoT por Vivienda vs Facturación.
    Une: comunidades JOIN viviendas JOIN sensores_iot JOIN lecturas_sensores.
    IMPORTANCIA: Cruza la telemetría de consumo de los sensores IoT con la estructura
    de la vivienda para detectar derroches energéticos o patrones anómalos.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    SELECT 
        c.nombre AS comunidad,
        v.numero_unidad,
        v.superficie_m2,
        s.tipo_sensor,
        s.ubicacion,
        ROUND(AVG(l.valor_medido), 2) AS promedio_consumo,
        MAX(l.valor_medido) AS consumo_pico,
        l.unidad_medida
    FROM comunidades c
    JOIN viviendas v ON c.id_comunidad = v.id_comunidad
    JOIN sensores_iot s ON v.id_vivienda = s.id_vivienda
    JOIN lecturas_sensores l ON s.id_sensor = l.id_sensor
    GROUP BY v.id_vivienda, s.id_sensor
    ORDER BY promedio_consumo DESC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    
    data = {
        "origen_base_datos": "PostgreSQL (cohousing_db)",
        "analisis": "Monitoreo de Eficiencia Energética e IoT por Vivienda",
        "justificacion_importancia": "Unir las comunidades, viviendas y lecturas de sensores IoT permite calcular la intensidad energética por metro cuadrado. Esto ayuda a detectar fugas de calefacción o fallos en electrodomésticos, garantizando la sostenibilidad y el ahorro energético en el complejo.",
        "metricas_eficiencia": []
    }
    
    for row in rows:
        data["metricas_eficiencia"].append({
            "comunidad": row[0],
            "vivienda": row[1],
            "superficie_m2": row[2],
            "tipo_sensor_iot": row[3],
            "ubicacion_sensor": row[4],
            "promedio_consumo_medido": row[5],
            "pico_maximo_registrado": row[6],
            "unidad_medida": row[7]
        })
        
    conn.close()
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Exportado informe JSON de PostgreSQL a: {output_json}")

def export_mariadb_analytics(db_path, output_json):
    """
    CONSULTA 3 (MariaDB): Impacto de Incidencias de Convivencia en Facturas y Gastos.
    Une: comunidades JOIN incidencias_convivencia JOIN residentes JOIN facturas_gastos_compartidos.
    IMPORTANCIA: Mide la relación entre las incidencias reportadas (averías/conflictos)
    y los gastos extraordinarios de mantenimiento de la comunidad.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    SELECT 
        c.nombre AS comunidad,
        i.titulo AS incidencia,
        i.prioridad,
        i.estado AS estado_incidencia,
        r.nombre || ' ' || r.apellidos AS reportado_por,
        f.concepto AS factura_asociada,
        f.monto_total AS importe_factura,
        f.estado_pago
    FROM comunidades c
    JOIN incidencias_convivencia i ON c.id_comunidad = i.id_comunidad
    JOIN residentes r ON i.id_residente_reporta = r.id_residente
    JOIN facturas_gastos_compartidos f ON c.id_comunidad = f.id_comunidad
    WHERE i.prioridad IN ('Media', 'Alta')
    ORDER BY f.monto_total DESC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    
    data = {
        "origen_base_datos": "MariaDB (cohousing_db)",
        "analisis": "Gestión de Incidencias de Convivencia y Coste de Mantenimiento",
        "justificacion_importancia": "Cruzar las incidencias graves reportadas por residentes con las facturas de la comunidad permite auditar el impacto económico de los desperfectos y averías. Facilita la asignación presupuestaria preventiva y la resolución transparente de conflictos comunitarios.",
        "auditoria_incidencias_gastos": []
    }
    
    for row in rows:
        data["auditoria_incidencias_gastos"].append({
            "comunidad": row[0],
            "incidencia_reportada": row[1],
            "prioridad": row[2],
            "estado_incidencia": row[3],
            "reportado_por_residente": row[4],
            "concepto_factura_comunitaria": row[5],
            "monto_factura_euros": row[6],
            "estado_pago": row[7]
        })
        
    conn.close()
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Exportado informe JSON de MariaDB a: {output_json}")

if __name__ == "__main__":
    export_mysql_analytics("mysql_cohousing.db", "analisis_afinidad_y_reservas_mysql.json")
    export_postgres_analytics("postgres_cohousing.db", "eficiencia_energetica_postgres.json")
    export_mariadb_analytics("mariadb_cohousing.db", "gestion_incidencias_mariadb.json")
