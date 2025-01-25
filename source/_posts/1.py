import os
import re

def add_banner_img_to_markdown(directory):
    """
    在指定目录下的所有 Markdown 文件中添加 banner_img 字段。
    banner_img 的值取自 cover 字段。
    :param directory: 文件所在目录
    """
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)

            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

            # 检查是否存在 cover 字段
            match = re.search(r"^cover:\s*(.+)$", content, flags=re.MULTILINE)
            if match:
                cover_value = match.group(1)
                
                # 检查是否已存在 banner_img 字段，避免重复添加
                if not re.search(r"^banner_img:\s*", content, flags=re.MULTILINE):
                    # 在 cover 字段后添加 banner_img
                    new_content = re.sub(
                        r"^(cover:\s*.+)$",
                        rf"\1\nbanner_img: {cover_value}",
                        content,
                        flags=re.MULTILINE
                    )

                    # 保存修改后的内容
                    with open(filepath, "w", encoding="utf-8") as file:
                        file.write(new_content)
                    
                    print(f"Processed: {filename}")
                else:
                    print(f"'banner_img' already exists in: {filename}")
            else:
                print(f"No 'cover' field found in: {filename}")

# 使用方法
if __name__ == "__main__":
    current_directory = os.getcwd()  # 当前目录
    add_banner_img_to_markdown(current_directory)