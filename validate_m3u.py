import os
import sys

def validate_m3u(file_path):
    print(f"Validating {file_path}...")
    errors = []
    warnings = []
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
        
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        first_line = f.readline().strip()
        if not first_line.startswith('#EXTM3U'):
            errors.append("Does not start with #EXTM3U")
            
        line_num = 1
        expecting_url = False
        last_extinf_line = 0
        
        url_count = 0
        extinf_count = 0
        
        for line in f:
            line_num += 1
            line = line.strip()
            
            if not line:
                continue
                
            if line.startswith('#EXTINF:'):
                if expecting_url:
                    warnings.append(f"Line {line_num}: #EXTINF block started before URL was found for previous #EXTINF on line {last_extinf_line}")
                expecting_url = True
                last_extinf_line = line_num
                extinf_count += 1
            elif not line.startswith('#'):
                # Assumed URL
                if not expecting_url and line_num > 2: # Ignore URL at top
                    warnings.append(f"Line {line_num}: URL found without preceding #EXTINF")
                expecting_url = False
                url_count += 1
    
    print("-" * 50)
    print(f"Summary for {file_path}:")
    print(f"Total #EXTINF tags: {extinf_count}")
    print(f"Total URLs: {url_count}")
    
    if errors:
        print("\nERRORS:")
        for e in errors[:20]:
            print(" - " + e)
        if len(errors) > 20: print(f" ... and {len(errors) - 20} more errors")
    else:
        print("\nNo critical errors found.")
        
    if warnings:
        print("\nWARNINGS:")
        for w in warnings[:20]:
            print(" - " + w)
        if len(warnings) > 20: print(f" ... and {len(warnings) - 20} more warnings")
    else:
        print("\nNo warnings found.")
        
if __name__ == "__main__":
    validate_m3u("lista.m3u")
