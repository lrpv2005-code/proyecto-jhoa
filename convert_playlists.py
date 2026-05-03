import os
import glob

def m3u_to_pls(m3u_path, pls_path):
    with open(m3u_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    files = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        files.append(line)

    with open(pls_path, 'w', encoding='utf-8') as f:
        f.write("[playlist]\n")
        for i, file_path in enumerate(files, 1):
            f.write(f"File{i}={file_path}\n")
            # Extract title from filename
            title = os.path.basename(file_path)
            f.write(f"Title{i}={title}\n")
            f.write(f"Length{i}=-1\n")
        f.write(f"NumberOfEntries={len(files)}\n")
        f.write("Version=2\n")

def main():
    source_dir = r"C:\Users\Jesus\Music\Playlist"
    output_dir = os.path.join(source_dir, "pls_format")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    m3u_files = glob.glob(os.path.join(source_dir, "*.m3u8"))
    print(f"Encontrados {len(m3u_files)} archivos .m3u8")

    for m3u_file in m3u_files:
        base_name = os.path.splitext(os.path.basename(m3u_file))[0]
        pls_file = os.path.join(output_dir, base_name + ".pls")
        try:
            m3u_to_pls(m3u_file, pls_file)
            print(f"Convertido: {base_name}.pls")
        except Exception as e:
            print(f"Error al convertir {m3u_file}: {e}")

if __name__ == "__main__":
    main()
