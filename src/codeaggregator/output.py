import os
import logging

logger = logging.getLogger(__name__)

def output_files(files, output_destination=None):
    output = []
    output.append("=" * 17)
    for file in files:
        # 存在チェック
        if os.path.exists(file):
            logger.info(f"Included: {file}")
        else:
            logger.warning(f"File does not exist: {file}")
            continue

        output.append(f"##################################\n{file}\n##################################\n")
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            output.append(content + "\n")
        except Exception as e:
            output.append(f"Error reading {file}: {e}\n")
    output.append("=" * 17)
    output_str = "\n".join(output)
    
    if output_destination:
        try:
            with open(output_destination, 'w', encoding='utf-8') as f:
                f.write(output_str)
        except Exception as e:
            print(f"Error writing to {output_destination}: {e}")
    else:
        print(output_str)
