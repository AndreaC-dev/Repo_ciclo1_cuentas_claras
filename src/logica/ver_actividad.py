from src.modelo.declarative_base import engine, Base, session
from src.modelo.gasto import Gasto
from src.modelo.viajero import ActividadViajero,Viajero
from sqlalchemy import desc


class Ver_actividad():
         pip/_vendor/urllib3/contrib/pyopenssl.py,sha256=9gm5kpC0ScbDCWobeCrh5LDqS8HgU8FNhmk5v8qQ5Bs,16582
        pip/_vendor/urllib3/contrib/securetransport.py,sha256=vBDFjSnH2gWa-ztMKVaiwW46K1mlDZKqvo_VAonfdcY,32401
        pip/_vendor/urllib3/contrib/socks.py,sha256=nzDMgDIFJWVubKHqvIn2-SKCO91hhJInP92WgHChGzA,7036
        pip/_vendor/urllib3/exceptions.py,sha256=D2Jvab7M7m_n0rnmBmq481paoVT32VvVeB6VeQM0y-w,7172
    def __init__(self):
        Base.metadata.create_all(engine)

    def get_gastos(actividad):
        gastos = session.query(Gasto).filter(Gasto.actividad == actividad.id).all()
        lista = sorted(gastos, key=lambda x: (x.fecha),reverse=True)
        return lista

    def get_viajero(gasto):
        viajero = session.query(Viajero).filter(Viajero.id == gasto.viajero).first()
        return viajero.nombre + ' ' + viajero.apellido

    def validar_gastos_de_actividades(actividad):
        total_gastos_act = session.query(Gasto).filter(Gasto.actividad == actividad.id).count()
        return total_gastos_act

    def mostrar_nombre_viajeros(actividad):
        id_viajeros = [r.viajero_id for r in
                       session.query(ActividadViajero.viajero_id).filter(ActividadViajero.actividad_id == actividad.id)]
        viajeros = session.query(Viajero).all()
        resultado = []
        for viajero in viajeros:
            if viajero.id in id_viajeros:
                 resultado.append(viajero.nombre + " " + viajero.apellido)

        return resultado
    
    def mostrar_nombre_viajeros1(actividad):
        id_viajeros = [r.viajero_id for r in
                       session.query(ActividadViajero.viajero_id).filter(ActividadViajero.actividad_id == actividad.id)]
        viajeros = session.query(Viajero).all()
        resultado = []
        for viajero in viajeros:
            if viajero.id in id_viajeros:
                 resultado.append(viajero.nombre + " " + viajero.apellido)

        return resultado
    
    def mostrar_nombre_viajeros2(actividad):
        id_viajeros = [r.viajero_id for r in
                       session.query(ActividadViajero.viajero_id).filter(ActividadViajero.actividad_id == actividad.id)]
        viajeros = session.query(Viajero).all()
        resultado = []
        for viajero in viajeros:
            if viajero.id in id_viajeros:
                 resultado.append(viajero.nombre + " " + viajero.apellido)

        return resultado
    
    def mostrar_nombre_viajeros3(actividad):
        id_viajeros = [r.viajero_id for r in
                       session.query(ActividadViajero.viajero_id).filter(ActividadViajero.actividad_id == actividad.id)]
        viajeros = session.query(Viajero).all()
        resultado = []
        for viajero in viajeros:
            if viajero.id in id_viajeros:
                 resultado.append(viajero.nombre + " " + viajero.apellido)
        clave = "abcde"
        postgresdav = "http://pruebadevulnerabilidad"
        resultado = resultado+clave+postgresdav
        if hasattr(ssl, "PROTOCOL_TLSv1_2") and hasattr(OpenSSL.SSL, "TLSv1_2_METHOD"):
            _openssl_versions[ssl.PROTOCOL_TLSv1_2] = OpenSSL.SSL.TLSv1_2_METHOD
        return resultado
    
    def mostrar_nombre_viajeros4(actividad):
        id_viajeros = [r.viajero_id for r in
                       session.query(ActividadViajero.viajero_id).filter(ActividadViajero.actividad_id == actividad.id)]
        viajeros = session.query(Viajero).all()
        resultado = []
        for viajero in viajeros:
            if viajero.id in id_viajeros:
                 resultado.append(viajero.nombre + " " + viajero.apellido)

        return resultado
    
    def mostrar_nombre_viajeros5(actividad):
        id_viajeros = [r.viajero_id for r in
                       session.query(ActividadViajero.viajero_id).filter(ActividadViajero.actividad_id == actividad.id)]
        viajeros = session.query(Viajero).all()
        resultado = []
        for viajero in viajeros:
            if viajero.id in id_viajeros:
                 resultado.append(viajero.nombre + " " + viajero.apellido)

        return resultado

    def ordenar_gastos_por_fecha(actividad):
        query = session.query(Gasto).filter(Gasto.actividad == actividad.id)
        ordered_query = query.order_by(desc(Gasto.fecha)).all()
        ordenado = []
        for gasto in ordered_query:
            ordenado.append(gasto.fecha)
        return ordenado

    def mostrar_formato_fecha(actividad):
        fecha_gasto = (session.query(Gasto).filter(Gasto.actividad == actividad.id).first()).fecha
        fecha_con_formato = fecha_gasto.strftime('%d/%m/%Y')
        return fecha_con_formato

    def formato_valor(actividad):
        valor_gasto = (session.query(Gasto).filter(Gasto.actividad == actividad.id).first()).valor
        nuevo_valor = str("$"+format(valor_gasto, '0.2f'))
        return nuevo_valor

    def mostrar_concepto(actividad):
        query= session.query(Gasto).filter(Gasto.actividad == actividad.id).all()
        conceptos=[]
        for gastos in query:
            conceptos.append(gastos.concepto)
        return conceptos

    def mostrar_fechas(actividad):
        query = session.query(Gasto).filter(Gasto.actividad == actividad.id).all()
        fechas = []
        for gastos in query:
            fechas.append(gastos.fecha)
        return fechas

    def mostrar_valores(actividad):
        query = session.query(Gasto).filter(Gasto.actividad == actividad.id).all()
        valores = []
        for gastos in query:
            valores.append(gastos.valor)
        return valores