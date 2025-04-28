import os
import openai
import json
import sys
from dotenv import load_dotenv

# Cargar variables de entorno (API KEY)
load_dotenv()

# Configurar la API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def comparar_oportunidades(descripcion1, descripcion2):
    """
    Compara dos descripciones de oportunidades de negocio utilizando GPT-4o-mini
    y retorna un porcentaje de similitud entre ellas.
    
    Args:
        descripcion1 (str): Primera descripción de oportunidad
        descripcion2 (str): Segunda descripción de oportunidad
        
    Returns:
        float: Porcentaje de similitud entre las descripciones
        str: Explicación detallada de la comparación
    """
    
    # Crear el prompt para GPT-4o-mini
    prompt = f"""
    Eres un experto en análisis legal y de negocios. Tu tarea es comparar dos oportunidades de negocio
    y determinar qué tan similares son en términos de sector, objetivos, alcance y requisitos.
    
    Oportunidad 1:
    {descripcion1}
    
    Oportunidad 2:
    {descripcion2}
    
    Evalúa detalladamente ambas oportunidades y proporciona:
    1. Un análisis punto por punto de sus similitudes y diferencias
    2. Un porcentaje numérico (de 0 a 100) que refleje el grado de similitud entre ambas
    3. Una breve justificación para el porcentaje asignado
    
    Responde en formato JSON con la siguiente estructura:
    {{
        "porcentaje_similitud": número,
        "analisis": "texto",
        "justificacion": "texto"
    }}
    """
    
    try:
        # Realizar la llamada a la API
        respuesta = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente especializado en análisis legal y comparación de oportunidades de negocio."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        
        # Extraer y parsear la respuesta JSON
        resultado = json.loads(respuesta.choices[0].message.content)
        
        return resultado["porcentaje_similitud"], resultado["analisis"], resultado["justificacion"]
    
    except Exception as e:
        print(f"Error al comparar las oportunidades: {e}")
        return 0, "", f"Error: {str(e)}"

def main():
    # Si se proporcionan argumentos desde línea de comandos
    if len(sys.argv) > 2:
        descripcion1 = sys.argv[1]
        descripcion2 = sys.argv[2]
    else:
        # Solicitar descripciones al usuario
        print("Introduce la descripción de la primera oportunidad de negocio:")
        descripcion1 = input()
        
        print("\nIntroduce la descripción de la segunda oportunidad de negocio:")
        descripcion2 = input()
    
    print("\nComparando oportunidades...")
    porcentaje, analisis, justificacion = comparar_oportunidades(descripcion1, descripcion2)
    
    print("\n" + "="*50)
    print(f"PORCENTAJE DE SIMILITUD: {porcentaje}%")
    print("="*50)
    print("\nANÁLISIS DETALLADO:")
    print(analisis)
    print("\nJUSTIFICACIÓN:")
    print(justificacion)
    print("="*50)

if __name__ == "__main__":
    main()
