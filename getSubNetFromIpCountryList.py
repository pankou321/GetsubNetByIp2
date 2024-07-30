def extract_cidr(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        cidr_value = None
        
        for line in infile:
            line = line.strip()
            if line.startswith('cidr:'):
                cidr_value = line.split('cidr:')[1].strip()
                outfile.write(f"{cidr_value}\n")
            elif line == '':
                # Skip empty lines to separate blocks
                continue

if __name__ == "__main__":
    input_file = 'blackipout.txt'
    output_file = 'blackip4postfix.txt'
    extract_cidr(input_file, output_file)
