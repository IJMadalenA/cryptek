import json as pyjson
import logging
import os
import random
import re

import environ
import google.generativeai as genai
from django.db.models import CharField, DateTimeField, Model, TextField

env = environ.Env()


class CodeTip(Model):
    """
    Modelo para almacenar consejos de código generados por Gemini.
    """

    title = CharField(max_length=255)
    description = TextField()
    code = TextField()
    tech_stack = CharField(
        choices=[("django", "Django"), ("python", "Python")],
        default="django",
    )
    type_of_tip = CharField(
        choices=[
            ("consejo", "Consejo"),
            ("tip", "Tip"),
            ("dato curioso", "Dato Curioso"),
            ("recomendación en ciberseguridad", "Recomendación en Ciberseguridad"),
        ],
        default="tip",
    )
    level = CharField(
        choices=[
            ("junior", "Junior"),
            ("mid", "Mid"),
            ("senior", "Senior"),
        ],
        default="junior",
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    prompt_used = TextField(blank=True, default="")
    gemini_raw_response = TextField(blank=True, default="")
    error_message = TextField(blank=True, default="")

    def __str__(self):
        return self.title

    @classmethod
    def generate_code_tip(cls, tech_stack=None, level=None, type_of_tip=None, save=True):
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

        tech_stack = tech_stack or random.choice(["django", "python"])
        level = level or random.choice(["junior", "mid", "senior"])
        type_of_tip = type_of_tip or random.choice(
            ["consejo", "tip", "dato curioso", "recomendación en ciberseguridad"]
        )
        prompt = (
            f"Dame un {type_of_tip} sobre {tech_stack} para un público de desarrolladores de nivel {level}. "
            "NO EXPLIQUES NADA FUERA DEL JSON. Solo responde con el JSON solicitado, sin texto adicional fuera de el. "
            "Devuelve única y exclusivamente una respuesta en formato JSON con los campos: title, description y code, "
            "donde 'code' es un fragmento de código relevante. Sé breve y útil para desarrolladores."
        )
        try:
            logger.info(f"Enviando prompt a Gemini: {prompt}")
            model = genai.GenerativeModel(env.str("GEMINI_MODEL", "gemini-2.5-pro-preview-03-25"))
            response = model.generate_content(prompt)
            text = response.text
            logger.warning(f"Respuesta cruda de Gemini: {text!r}")
            cleaned = re.sub(
                r"^```(?:json)?[ \t]*\n?|```$", "", text.strip(), flags=re.IGNORECASE | re.MULTILINE
            ).strip()
            logger.warning(f"Respuesta limpia para parsear: {cleaned!r}")
            tip = None
            error = None
            try:
                tip = pyjson.loads(cleaned)
            except Exception as e1:
                json_match = re.search(r"{[\s\S]*}", cleaned)
                if json_match:
                    try:
                        tip = pyjson.loads(json_match.group(0))
                    except Exception as e2:
                        error = f"Error al parsear JSON extraído: {e2}"
                else:
                    error = f"Error al parsear JSON directo: {e1}"
            if tip and isinstance(tip, dict):
                logger.info(f"Tip recibido: {tip}")
                tip = {
                    "title": tip.get("title", "Tip de Gemini"),
                    "description": tip.get("description", ""),
                    "code": tip.get("code", ""),
                }
                if save:
                    # Evita duplicados simples (por título y código)
                    obj, created = cls.objects.get_or_create(
                        title=tip["title"],
                        code=tip["code"],
                        defaults={
                            "description": tip["description"],
                            "tech_stack": tech_stack,
                            "level": level,
                            "type_of_tip": type_of_tip,
                            "prompt_used": prompt,
                            "gemini_raw_response": text,
                            "error_message": "",
                        },
                    )
                return tip
            else:
                logger.error(f"Respuesta NO JSON de Gemini (tras limpieza): {cleaned!r}")
                if save:
                    cls.objects.create(
                        title="Respuesta no estructurada",
                        description=cleaned,
                        code=f"# Error al parsear JSON: {error if error else 'No se encontró JSON válido'}",
                        tech_stack=tech_stack,
                        level=level,
                        type_of_tip=type_of_tip,
                        prompt_used=prompt,
                        gemini_raw_response=text,
                        error_message=error or "No se encontró JSON válido",
                    )
                return {
                    "title": "Respuesta no estructurada",
                    "description": cleaned,
                    "code": f"# Error al parsear JSON: {error if error else 'No se encontró JSON válido'}",
                }
        except Exception as e:
            logger.error(f"Error al obtener tip de Gemini: {e}")
            if save:
                cls.objects.create(
                    title="Error al obtener tip de Gemini",
                    description=str(e),
                    code="# Error en la llamada a Gemini",
                    tech_stack=tech_stack,
                    level=level,
                    type_of_tip=type_of_tip,
                    prompt_used=prompt,
                    gemini_raw_response=text if "text" in locals() else "",
                    error_message=str(e),
                )
            return {
                "title": "Error al obtener tip de Gemini",
                "description": str(e),
                "code": "# Error en la llamada a Gemini",
            }
