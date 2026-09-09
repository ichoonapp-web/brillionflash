import re

def clean_env():
    with open('.env', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    for line in lines:
        # Remove Windows line endings
        line = line.rstrip('\r\n')
        # Skip empty lines
        if not line.strip():
            continue
        # Keep comments (lines starting with #)
        if line.strip().startswith('#'):
            cleaned_lines.append(line)
            continue
        # Skip lines that don't have '=' (not a valid KEY=VALUE)
        if '=' not in line:
            continue
        # Skip lines that contain a comma (usually from copied code)
        if ',' in line:
            continue
        # If line is valid, keep it
        cleaned_lines.append(line)
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_lines) + '\n')
    
    print("✅ .env cleaned successfully!")

if __name__ == "__main__":
    clean_env()