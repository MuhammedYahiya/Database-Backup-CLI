import zipfile
import os

def compress_file(file_path, output_zip_path):
    """
    Compress any file into a .zip archive.
    
    Args:
        file_path (str): Path to the original file to compress.
        output_zip_path (str): Path where the .zip archive should be saved.
    
    Returns:
        str or None: Path to the compressed .zip file if successful, None otherwise.
    """
    try:
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path, os.path.basename(file_path))
        os.remove(file_path)
        print(f"Compressed and removed original file: {file_path}")
        return output_zip_path
    except Exception as e:
        print(f"Compression failed: {e}")
        return None
