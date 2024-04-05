import os
import sys

# Thêm đường dẫn của thư mục cha vào sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(parent_dir)

print(parent_dir)
