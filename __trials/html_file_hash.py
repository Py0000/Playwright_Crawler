import hashlib

def compute_hash(file_path, algorithm='sha256'):
    """Compute hash of a file using the given algorithm."""
    h = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        # Reading in chunks in case of large files
        for chunk in iter(lambda: f.read(4096), b''):
            h.update(chunk)
    return h.hexdigest()

file1_hash = compute_hash('html_script_aft.html')
file2_hash = compute_hash('html_script_before (1).html')

if file1_hash == file2_hash:
    print("The two files are identical.")
else:
    print("The two files are different.")
