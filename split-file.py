def split_file(file_path, lines_per_file):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    total_lines = len(lines)
    file_count = (total_lines + lines_per_file - 1) // lines_per_file

    for i in range(file_count):
        start = i * lines_per_file
        end = start + lines_per_file
        chunk = lines[start:end]

        output_file_path = f"{file_path}_part{i+1}.txt"
        with open(output_file_path, 'w') as output_file:
            output_file.writelines(chunk)

        print(f"Created file: {output_file_path}")

# Example usage:
split_file('hillary-clinton-emails-august-31-release_djvu.txt.html', 1000)  # Split 'input.txt' into files with 1000 lines each