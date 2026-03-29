def split_m3u(input_file):
    print(f"Lendo {input_file}...")
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Erro: Arquivo {input_file} não encontrado.")
        return

    canais = []
    filmes = []
    series = []
    
    header = "#EXTM3U\n"
    if lines and lines[0].startswith("#EXTM3U"):
        header = lines[0]

    canais.append(header)
    filmes.append(header)
    series.append(header)

    i = 0
    count_canais = 0
    count_filmes = 0
    count_series = 0

    while i < len(lines):
        line = lines[i].strip()
        
        # Ignora linhas em branco
        if not line:
            i += 1
            continue
            
        if line.startswith("#EXTINF:"):
            extinf_line = lines[i]
            url_line = ""
            
            # Pega a próxima linha que não for um #EXT
            j = i + 1
            while j < len(lines):
                if not lines[j].strip().startswith("#"):
                    url_line = lines[j]
                    break
                j += 1
                
            if url_line:
                # Classifica baseado na URL:
                # URLs de filmes tem /movie/ e URLs de séries tem /series/
                if "/movie/" in url_line:
                    filmes.append(extinf_line)
                    filmes.append(url_line)
                    count_filmes += 1
                elif "/series/" in url_line:
                    series.append(extinf_line)
                    series.append(url_line)
                    count_series += 1
                else:
                    canais.append(extinf_line)
                    canais.append(url_line)
                    count_canais += 1
            
            i = j + 1
        else:
            i += 1

    print(f"Salvando Canais.m3u ({count_canais} itens)...")
    with open('Canais.m3u', 'w', encoding='utf-8') as f:
        f.writelines(canais)
        
    print(f"Salvando Filmes.m3u ({count_filmes} itens)...")
    with open('Filmes.m3u', 'w', encoding='utf-8') as f:
        f.writelines(filmes)
        
    print(f"Salvando Series.m3u ({count_series} itens)...")
    with open('Series.m3u', 'w', encoding='utf-8') as f:
        f.writelines(series)
        
    print("\nSeparação concluída com sucesso!")
    print("Os filmes (VOD) foram identificados e separados corretamente através da estrutura URL (/movie/).")

if __name__ == '__main__':
    split_m3u('lista.m3u')
