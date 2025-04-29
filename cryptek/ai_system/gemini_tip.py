import logging
import os
import random

import environ
import google.generativeai as genai

env = environ.Env()


def get_gemini_tip(prompt=None):
    logger = logging.getLogger("gemini_tip")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.error("Gemini API Key no configurada.")
        return {
            "title": "Gemini API Key no configurada",
            "description": "Por favor, configura la variable de entorno GEMINI_API_KEY.",
            "code": "# Sin clave de API",
        }

    genai.configure(api_key=api_key)

    tech = random.choice(["django", "python"])
    level = random.choice(["junior", "mid", "senior"])
    if not prompt:
        prompt = (
            f"Dame un consejo, tip o dato curioso sobre {tech} para un público de nivel {level}. "
            "NO EXPLIQUES NADA. Solo responde con el JSON solicitado, sin texto adicional. "
            "Devuelve única y exclusivamente una respuesta en formato JSON con los campos: title, description y code, "
            "donde code es un fragmento de código relevante. Sé breve y útil para desarrolladores."
        )

    try:
        logger.info(f"Enviando prompt a Gemini: {prompt}")
        model = genai.GenerativeModel(env.str("GEMINI_MODEL", "gemini-2.5-pro-preview-03-25"))
        response = model.generate_content(prompt)
        text = response.text
        logger.warning(f"Respuesta cruda de Gemini: {text!r}")
        import json as pyjson
        import re
        # Elimina cualquier bloque de código markdown (```json ... ``` o ``` ... ```)
        cleaned = re.sub(r"^```(?:json)?[ \t]*\n?|```$", "", text.strip(), flags=re.IGNORECASE | re.MULTILINE).strip()
        logger.warning(f"Respuesta limpia para parsear: {cleaned!r}")
        # Intenta extraer el JSON aunque esté incrustado en texto
        tip = None
        error = None
        # 1. Intenta parsear directamente
        try:
            tip = pyjson.loads(cleaned)
        except Exception as e1:
            # 2. Busca el primer bloque JSON válido en el texto limpio
            json_match = re.search(r'{[\s\S]*}', cleaned)
            if json_match:
                try:
                    tip = pyjson.loads(json_match.group(0))
                except Exception as e2:
                    error = f"Error al parsear JSON extraído: {e2}"
            else:
                error = f"Error al parsear JSON directo: {e1}"
        if tip and isinstance(tip, dict):
            logger.info(f"Tip recibido: {tip}")
            # Normaliza los campos esperados
            return {
                "title": tip.get("title", "Tip de Gemini"),
                "description": tip.get("description", ""),
                "code": tip.get("code", "")
            }
        else:
            logger.error(f"Respuesta NO JSON de Gemini (tras limpieza): {cleaned!r}")
            return {
                "title": "Respuesta no estructurada",
                "description": cleaned,
                "code": f"# Error al parsear JSON: {error if error else 'No se encontró JSON válido'}"
            }
    except Exception as e:
        logger.error(f"Error al obtener tip de Gemini: {e}")
        return {
            "title": "Error al obtener tip de Gemini",
            "description": str(e),
            "code": "# Error en la llamada a Gemini",
        }
