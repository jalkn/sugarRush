import os
from PIL import Image

def redimensionar_imagen(ruta_imagen, ancho=800, alto=800):
    try:
        # Verificar si el archivo existe
        if not os.path.exists(ruta_imagen):
            print(f"Error: No se encontró el archivo en '{ruta_imagen}'")
            return

        # Abrir la imagen
        with Image.open(ruta_imagen) as img:
            # Redimensionar la imagen a los píxeles exactos
            # Usamos Image.Resampling.LANCZOS para mantener la mejor calidad posible
            img_redimensionada = img.resize((ancho, alto), Image.Resampling.LANCZOS)
            
            # Generar el nombre del nuevo archivo (ej: imagen_800x800.jpg)
            nombre_base, extension = os.path.splitext(ruta_imagen)
            nueva_ruta = f"{nombre_base}_{ancho}x{alto}{extension}"
            
            # Guardar la imagen
            img_redimensionada.save(nueva_ruta)
            print(f"¡Éxito! Imagen guardada en: {nueva_ruta}")
            
    except Exception as e:
        print(f"Ocurrió un error al procesar la imagen: {e}")

# --- EJEMPLO DE USO ---
# Solo cambia 'tu_imagen.png' o 'tu_imagen.jpg' por la ruta de tu archivo
ruta_de_mi_imagen = "img/caps.png" 
redimensionar_imagen(ruta_de_mi_imagen)