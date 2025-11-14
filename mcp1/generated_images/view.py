from PIL import Image

try:
    # BytesIOではなく、ファイルパスから直接開く
    img = Image.open('tiny_image_20251114_220346.png')
    print(f"✅ Successfully opened!")
    print(f"Size: {img.size}")
    print(f"Mode: {img.mode}")
    print(f"Format: {img.format}")
    
    # 拡大して保存
    img_large = img.resize((200, 200), Image.NEAREST)
    img_large.save('tiny_image_large.png')
    print("Saved enlarged version as tiny_image_large.png")
    
    # 別の形式でも保存してみる
    img_large.save('tiny_image_large.jpg', 'JPEG')
    print("Also saved as tiny_image_large.jpg")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()