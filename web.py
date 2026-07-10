import streamlit as st
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO

# 1. Configuración de la plataforma
st.set_page_config(page_title="Panel Administrador 10 en 1", page_icon="⚙️", layout="centered")

st.title("⚙️ Sistema Multi-Herramientas para Dueños de Restaurantes")
st.write("La suite administrativa con 10 funciones esenciales para el control del negocio.")

st.markdown("---")

# 2. Organización del panel en 3 grandes pestañas de control
pestana1, pestana2, pestana3 = st.tabs(["🖨️ Módulo QR (Funciones 1 a 5)", "🥩 Módulo Costos (Funciones 6 a 8)", "🧾 Módulo Caja (Funciones 9 y 10)"])

# =====================================================================
# PESTAÑA 1: MÓDULO QR (FUNCIONES 1 A 5)
# =====================================================================
with pestana1:
    st.subheader("📊 Control y Creación de Códigos QR")
    
    opcion_qr = st.selectbox("Elige qué tipo de código QR comercial deseas fabricar hoy:", [
        "Función 1: Enlace Web (Instagram o Menú Digital)", 
        "Función 2: Conexión Wi-Fi automática para Clientes", 
        "Función 3: Sistema para Llamar al Mesero (WhatsApp)",
        "Función 4: Sistema para Pedir la Cuenta (WhatsApp)",
        "Función 5: Tarjeta de Reseñas de 5 Estrellas (Google Maps)"
    ])
    
    # Lógica interna para configurar los datos de los 5 tipos de QR
    if "Función 1" in opcion_qr:
        datos_qr = st.text_input("🔗 Pega el link de la carta web o perfil de Instagram:", "https://instagram.com")
    elif "Función 2" in opcion_qr:
        nombre_red = st.text_input("Nombre de la Red Wi-Fi (SSID):", "WiFi_Restaurante")
        clave_red = st.text_input("Contraseña del Wi-Fi del local:", "12345678", type="password")
        datos_qr = f"WIFI:S:{nombre_red};T:WPA;P:{clave_red};;"
    elif "Función 3" in opcion_qr:
        num_mesa = st.text_input("Número de Mesa (ej: Mesa 3):", "Mesa 3")
        telefono = st.text_input("WhatsApp de la Barra/Cocina:", "56912345678")
        datos_qr = f"https://wa.me{telefono}?text=Hola,%20necesitamos%20asistencia%20en%20la%20{num_mesa.replace(' ', '%20')}"
    elif "Función 4" in opcion_qr:
        num_mesa_c = st.text_input("Número de Mesa que pide la cuenta:", "Mesa 3")
        metodo = st.selectbox("Método de pago seleccionado:", ["Tarjeta", "Efectivo", "Transferencia"])
        telefono_c = st.text_input("WhatsApp de la Caja Registradora:", "56912345678")
        datos_qr = f"https://wa.me{telefono_c}?text=Hola,%20cuenta%20para%20la%20{num_mesa_c.replace(' ', '%20')}.%20Pagaremos%20con%20{metodo}"
    else:
        datos_qr = st.text_input("🔗 Enlace directo de reseñas de tu ficha de Google Maps:", "https://g.page")

    color_qr = st.color_picker("Elige el color del QR corporativo:", "#000000")
    icono_centro = st.selectbox("Icono del centro del código:", ["🍔", "🍕", "☕", "🥩"])

    if st.button("🔥 GENERAR QR COMERCIAL"):
        qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=3)
        qr.add_data(datos_qr)
        img = qr.make_image(fill_color=color_qr, back_color="#FFFFFF").convert("RGB")
        
        # Estilo del icono en medio
        w, h = img.size
        dibujo = ImageDraw.Draw(img)
        dibujo.ellipse([w//2-25, h//2-25, w//2+25, h//2+25], fill=color_qr)
        dibujo.text((w//2, h//2), icono_centro, fill="#FFFFFF", anchor="mm")
        
        buffer_qr = BytesIO()
        img.save(buffer_qr, format="PNG")
        
        st.success("🎉 ¡Código QR generado con éxito!")
        st.image(buffer_qr.getvalue(), width=300)
        st.download_button("📥 Descargar QR para Imprenta (PNG)", buffer_qr.getvalue(), "qr_restaurante.png")

# =====================================================================
# PESTAÑA 2: MÓDULO COSTOS (FUNCIONES 6 A 8)
# =====================================================================
with pestana2:
    st.subheader("🥩 Control Financiero de Platos y Recetas")
    
    # ¡LÍNEA CORREGIDA AQUÍ! Ahora se desempaquetan las 3 columnas perfectamente
    col1, col2, col3 = st.columns(3)
    with col1:
        costo_ingredientes = st.number_input("Costo de alimentos de la receta:", min_value=0, value=2500)
    with col2:
        costo_empaque = st.number_input("Costo de insumos (servilletas/bolsas):", min_value=0, value=300)
    with col3:
        gastos_servicios = st.number_input("Gasto de servicios (gas/luz/agua por plato):", min_value=0, value=400)
        
    precio_venta = st.number_input("¿A qué precio vendes este plato al público actualmente?:", min_value=1, value=7500)
    
    # Cálculo automático de costos totales
    costo_total = costo_ingredientes + costo_empaque + gastos_servicios
    
    # FUNCIÓN 6: CALCULADORA DE MARGEN DE GANANCIA NETO
    ganancia_neta = precio_venta - costo_total
    porcentaje_g = (ganancia_neta / precio_venta) * 100 if precio_venta > 0 else 0
    st.markdown(f"### 💰 Costo Neto de Fabricación: **${costo_total:,}**")
    
    # FUNCIÓN 7: SISTEMA AUTOMÁTICO DE ALERTAS DE PÉRDIDAS
    if ganancia_neta <= 0:
        st.error(f"🚨 ¡ALERTA DE PÉRDIDA! Estás perdiendo **${abs(ganancia_neta):,}** en este plato. ¡Ajusta el precio hoy mismo!")
    elif porcentaje_g < 55:
        st.warning(f"⚠️ Atención: Tu ganancia por plato es de **${ganancia_neta:,}** ({porcentaje_g:.1f}%). Margen comercial bajo para gastronomía.")
    else:
        st.success(f"✅ ¡Operación saludable! Ganancia neta por plato: **${ganancia_neta:,}** ({porcentaje_g:.1f}%).")
        
    st.markdown("---")
    
    # FUNCIÓN 8: PROYECCIONES DE RIQUEZA MENSUAL
    st.write("📊 **Simulador de Ventas Mensuales**")
    platos_mes = st.slider("¿Cuántos platos de estos se venden al mes en promedio?:", min_value=10, max_value=2000, value=400)
    riqueza_mensual = ganancia_neta * platos_mes
    
    if riqueza_mensual > 0:
        st.info(f"🏦 **Proyección: Este plato le dejará al negocio una ganancia mensual neta de:** ${riqueza_mensual:,}")
    else:
        st.error(f"📉 **Proyección de Pérdida:** Tu negocio perderá **${abs(riqueza_mensual):,}** al mes si mantienes este precio.")

# =====================================================================
# PESTAÑA 3: MÓDULO CAJA (FUNCIONES 9 Y 10)
# =====================================================================
with pestana3:
    st.subheader("🧾 Contabilidad de Caja e Impuestos Rápidos")
    
    porcentaje_iva = st.selectbox("Elige la tasa de impuesto local (IVA %):", [19, 16, 12, 21], index=0)
    tipo_calculo = st.radio("¿Qué operación contable vas a realizar?:", ["A. Desglosar desde precio NETO", "B. Desglosar desde precio TOTAL"])
    
    if tipo_calculo == "A. Desglosar desde precio NETO":
        monto_neto = st.number_input("Monto Neto de los productos ingresados ($):", min_value=0, value=10000)
        
        # FUNCIÓN 9: CÁLCULO AUTOMÁTICO DE VALOR DE IVA
        calculo_iva = monto_neto * (porcentaje_iva / 100)
        # FUNCIÓN 10: CÁLCULO DE TOTALES PARA HACER LA BOLETA
        monto_total = monto_neto + calculo_iva
    else:
        monto_total = st.number_input("Monto Total cobrado al cliente ($):", min_value=0, value=11900)
        
        # FUNCIÓN 10: CÁLCULO DE BASE DESDE TOTAL INCLUIDO
        monto_neto = monto_total / (1 + (porcentaje_iva / 100))
        # FUNCIÓN 9: EXTRACCIÓN DE IVA
        calculo_iva = monto_total - monto_neto

    # Desglose en pantalla
    st.markdown("### 📋 Datos Contables de la Operación:")
    st.write(f"🔹 **Base Neta (Sin impuesto):** ${monto_neto:,.0f}")
    st.write(f"🔹 **Impuesto Retenido (IVA {porcentaje_iva}%):** ${calculo_iva:,.0f}")
    st.markdown(f"## 💰 Monto Final de la Boleta: **${monto_total:,.0f}**")
