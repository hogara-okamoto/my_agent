import struct

with open('tiny_image_20251114_220346.png', 'rb') as f:
    data = f.read()
    
    print(f"File size: {len(data)} bytes")
    
    # PNGシグネチャをチェック
    signature = data[:8]
    print(f"\nPNG Signature: {signature.hex()}")
    print(f"Expected:      89504e470d0a1a0a")
    expected_sig = bytes([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a])
    print(f"Valid: {signature == expected_sig}")
    
    # 最初の数チャンクを解析
    pos = 8
    chunk_count = 0
    while pos < len(data) and chunk_count < 10:
        if pos + 8 > len(data):
            break
            
        length = struct.unpack('>I', data[pos:pos+4])[0]
        chunk_type = data[pos+4:pos+8]
        
        print(f"\nChunk {chunk_count}:")
        print(f"  Position: {pos}")
        print(f"  Type: {chunk_type}")
        print(f"  Length: {length}")
        
        # IHDRの場合、詳細を表示
        if chunk_type == b'IHDR':
            width = struct.unpack('>I', data[pos+8:pos+12])[0]
            height = struct.unpack('>I', data[pos+12:pos+16])[0]
            bit_depth = data[pos+16]
            color_type = data[pos+17]
            compression = data[pos+18]
            filter_method = data[pos+19]
            interlace = data[pos+20]
            
            print(f"    Width: {width}")
            print(f"    Height: {height}")
            print(f"    Bit depth: {bit_depth}")
            print(f"    Color type: {color_type}")
            print(f"    Compression: {compression}")
            print(f"    Filter: {filter_method}")
            print(f"    Interlace: {interlace}")
        
        # 次のチャンクへ
        pos += 4 + 4 + length + 4
        chunk_count += 1
    
    print(f"\nTotal chunks found: {chunk_count}")
    print(f"File ends at position: {len(data)}")
    print(f"Last 12 bytes: {data[-12:].hex()}")