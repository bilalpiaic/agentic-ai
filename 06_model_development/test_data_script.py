import os
import random
import shutil

def move_images(src_dir, dest_dir, test_ratio=0.2):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    images = [f for f in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, f))]
    num_test = int(len(images) * test_ratio)
    test_images = random.sample(images, num_test)

    for img in test_images:
        src_path = os.path.join(src_dir, img)
        dest_path = os.path.join(dest_dir, img)
        shutil.move(src_path, dest_path)

    print(f"Moved {len(test_images)} images from {src_dir} to {dest_dir}")

# Set paths
base_dir = "dataset"
train_dir = os.path.join(base_dir, "train")
val_dir = os.path.join(base_dir, "validation")

# For both categories
for category in ["cats", "dogs"]:
    move_images(
        src_dir=os.path.join(train_dir, category),
        dest_dir=os.path.join(val_dir, category),
        test_ratio=0.2  # 20% to validation
    )
