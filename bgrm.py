from PIL import Image, ImageDraw, ImageFilter

def cambiar_fondo_y_recortar(input_path, output_path, umbral_blanco=238, radio_suavizado=1.2, tolerancia_flood=30):
    # 1. Cargar imagen original
    img = Image.open(input_path).convert("RGBA")
    
    # 2. Reemplazar el fondo blanco exterior mediante Flood Fill desde la esquina (0,0)
    # Usamos Magenta (#FF00FF) para no interferir con los tonos verdes de las hojas
    color_chroma = (255, 0, 255, 255)
    ImageDraw.floodfill(img, (0, 0), color_chroma, thresh=tolerancia_flood)
    
    # 3. Generar la máscara Alpha: lo que sea Magenta pasa a ser 0 (transparente)
    datas = img.getdata()
    alpha_data = []
    for r, g, b, a in datas:
        if r > 200 and g < 50 and b > 200:  # Detecta el color Chroma
            alpha_data.append(0)
        else:
            alpha_data.append(255)
            
    # Crear imagen de máscara
    mask = Image.new("L", img.size)
    mask.putdata(alpha_data)
    
    # 4. Aplicar difuminado gaussiano liviano a la máscara para suavizar bordes (Anti-aliasing)
    mask_smooth = mask.filter(ImageFilter.GaussianBlur(radius=radio_suavizado))
    
    # 5. Asignar la máscara suavizada a la imagen
    img.putalpha(mask_smooth)
    
    # 6. Recortar bordes sobrantes ajustados a los límites del logo
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    img.save(output_path, "PNG")
    print(f"PNG de alta precisión guardado exitosamente en: {output_path}")

# Ejemplo de uso:
cambiar_fondo_y_recortar("img/logo.jpeg", "img/logo.png", radio_suavizado=1.2)