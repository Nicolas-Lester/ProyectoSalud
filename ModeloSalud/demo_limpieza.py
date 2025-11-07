# Script de demostración de limpieza de texto
# Ejecutar con: python manage.py shell < demo_limpieza.py

from sentimientos.servicios import limpiar_texto

print("=" * 80)
print("🧹 DEMOSTRACIÓN DE LIMPIEZA DE TEXTO")
print("=" * 80)
print()

# Ejemplos del CSV real
ejemplos = [
    "EXCELENTE atencion medica!!! 😊😊 El doctor fue muy muy muy profesional y amable con mi familia @hospital",
    "Pesimo servicio... Tuve q esperar mas de 3 HORAS para ser atendido!!! 😡😡😡",
    "Muy buena experiencia!! Todo el personal fue super atento y comprensivo 👍👍",
    "La enfermera fue MUY GROSERA y no respondio mis preguntas?? que mal servicio de verdad",
    "Instalaciones muy muy limpias y modernas ✨✨ Me senti comodo durante la visita",
    "NO RECOMIENDO este hospital!! El trato fue horrible horrible y descuidado 👎",
    "WOW!!! El mejor hospital hospital en el q he estado 😍😍 Super recomendado @todos",
    "Que pesimo servicio de verdad verdad!!! No vuelvo nunca mas aca 😡",
    "Super agradecido agradecido con todo el personal 🙏❤️ Salvaron a mi mama",
    "Las camas son incomodas y viejas 🛏️ Necesitan renovar renovar TODO",
]

for i, texto_original in enumerate(ejemplos, 1):
    print(f"📝 EJEMPLO {i}")
    print("-" * 80)
    print(f"ORIGINAL ({len(texto_original)} caracteres):")
    print(f"  {texto_original}")
    print()
    
    texto_limpio = limpiar_texto(texto_original)
    
    print(f"LIMPIO ({len(texto_limpio)} caracteres):")
    print(f"  {texto_limpio}")
    print()
    
    # Análisis
    emojis_removidos = len([c for c in texto_original if ord(c) > 127])
    mayusculas_removidas = sum(1 for c in texto_original if c.isupper())
    simbolos_removidos = len([c for c in texto_original if c in '!?@.,-;:'])
    
    print(f"📊 ESTADÍSTICAS:")
    print(f"  • Emojis/caracteres especiales removidos: {emojis_removidos}")
    print(f"  • Mayúsculas normalizadas: {mayusculas_removidas}")
    print(f"  • Símbolos de puntuación removidos: {simbolos_removidos}")
    print(f"  • Reducción de longitud: {len(texto_original) - len(texto_limpio)} caracteres ({((len(texto_original) - len(texto_limpio)) / len(texto_original) * 100):.1f}%)")
    print()
    print("=" * 80)
    print()

print("✅ DEMOSTRACIÓN COMPLETADA")
print()
print("📈 RESUMEN GENERAL:")
print("  • Total de ejemplos procesados: 10")
print("  • Elementos removidos: emojis, mayúsculas, símbolos, repeticiones, stopwords")
print("  • Texto normalizado y listo para el modelo de IA")
