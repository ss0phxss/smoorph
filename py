import argparse
import pyfiglet

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary_str):
    chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def encode(original_file, secret_message, output_file):
    with open(original_file, 'r') as f:
        original_text = f.read()

    # Convert secret message to binary
    binary_message = text_to_binary(secret_message)
    
    encoded_text = ""
    binary_index = 0

    for char in original_text:
        encoded_text += char
        if char in [' ', '\n', '\t'] and binary_index < len(binary_message):
            if binary_message[binary_index] == '1':
                encoded_text += '\u200A'  # Hair space (invisible)
            binary_index += 1

    # Add remaining binary message at the end if there's space
    while binary_index < len(binary_message):
        encoded_text += ' '
        if binary_message[binary_index] == '1':
            encoded_text += '\u200A'  # Hair space
        binary_index += 1

    with open(output_file, 'w') as f:
        f.write(encoded_text)
    print(f"Encoded file '{output_file}' created with the secret message hidden.")

def decode(encoded_file):
    with open(encoded_file, 'r') as f:
        encoded_text = f.read()

    binary_message = ""

    for i, char in enumerate(encoded_text):
        if char == '\u200A':  # Hair space (invisible)
            binary_message += '1'
        elif char in [' ', '\n', '\t']:
            if i + 1 < len(encoded_text) and encoded_text[i + 1] == '\u200A':
                continue
            else:
                binary_message += '0'
        else:
            continue
    
    secret_message = binary_to_text(binary_message)
    return secret_message

def main():
    banner = pyfiglet.figlet_format("Smoorph")
    print(banner)

    parser = argparse.ArgumentParser(description="Smoorph: A Steganography Tool")
    subparsers = parser.add_subparsers(dest='command', help="Commands")

    # Sub-parser for the encode command
    encode_parser = subparsers.add_parser('encode', help="Encode a secret message")
    encode_parser.add_argument('original_file', type=str, help="Path to the original text file")
    encode_parser.add_argument('secret_message', type=str, help="Secret message to hide")
    encode_parser.add_argument('output_file', type=str, help="Path to save the encoded file")

    # Sub-parser for the decode command
    decode_parser = subparsers.add_parser('decode', help="Decode a secret message")
    decode_parser.add_argument('encoded_file', type=str, help="Path to the encoded file")

    args = parser.parse_args()

    if args.command == 'encode':
        encode(args.original_file, args.secret_message, args.output_file)
    elif args.command == 'decode':
        secret_message = decode(args.encoded_file)
        print(f"Decoded secret message:\n{secret_message}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
