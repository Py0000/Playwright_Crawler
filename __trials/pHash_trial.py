from PIL import Image
import imagehash

def compute_phash(image_path):
    with Image.open(image_path) as img:
        hash_val = imagehash.phash(img)
    return hash_val

# Example usage
hash1 = compute_phash("screenshot_aft.png")
hash2 = compute_phash("screenshot_aft (1).png")

# Compute hash difference (0 means identical, small values mean similar)
diff = hash1 - hash2

print("Hash 1:", hash1)
print("Hash 2:", hash2)
print("Difference between images:", diff)
