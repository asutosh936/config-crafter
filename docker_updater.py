import sys
import os
import re

def delete_lines_from_dockerfile(dockerfile_path, search_content, multiline=False, backup=True):
    """
    Search for specific content in a Dockerfile and delete entire lines containing it.
    Also prints the deleted lines.
    
    Parameters:
    - dockerfile_path: Path to the Dockerfile
    - search_content: Content to search for in lines to delete
    - multiline: Whether to handle multiline instructions with backslash continuations
    - backup: Whether to create a backup file (default: True)
    
    Returns:
    - True if successful, False otherwise
    """
    # Create backup if requested
    if backup:
        backup_file = f"{dockerfile_path}.bak"
        with open(dockerfile_path, 'r') as src, open(backup_file, 'w') as dst:
            dst.write(src.read())
        print(f"Backup created: {backup_file}")
    
    # Read the file content as lines
    with open(dockerfile_path, 'r') as f:
        lines = f.readlines()
    
    # Keep original lines for comparison
    original_lines = lines.copy()
    deleted_lines = []  # Store deleted lines here
    
    if multiline:
        # Handle multiline instructions (with backslash continuations)
        new_lines = []
        skip_line = False
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Check if this line contains the search content
            if search_content in line:
                skip_line = True
                current_deleted_block = [line]  # Start tracking this deleted block
                
                # Skip this line and all continuation lines
                while i < len(lines) and line.strip().endswith('\\'):
                    i += 1
                    if i < len(lines):
                        line = lines[i]
                        current_deleted_block.append(line)  # Add continuation line to deleted block
                
                # Add the complete deleted block to our list of deleted lines
                deleted_lines.extend(current_deleted_block)
                i += 1
                skip_line = False
                continue
            
            # Check if it's a continuation of a line we're skipping
            if skip_line and line.strip().endswith('\\'):
                deleted_lines.append(line)
                i += 1
                continue
            
            # Otherwise, keep the line
            new_lines.append(line)
            i += 1
            
        lines = new_lines
    else:
        # Simple line-by-line deletion
        new_lines = []
        for line in lines:
            if search_content in line:
                deleted_lines.append(line)
            else:
                new_lines.append(line)
        lines = new_lines
    
    # Check if any changes were made
    if lines == original_lines:
        print(f"Warning: Content '{search_content}' not found in {dockerfile_path}")
        return False
    
    # Write the updated content back
    with open(dockerfile_path, 'w') as f:
        f.writelines(lines)
    
    # Print the deleted lines
    if deleted_lines:
        print("\nDeleted lines:")
        for i, line in enumerate(deleted_lines, 1):
            print(f"{i}: {line.rstrip()}")
    
    print(f"Successfully deleted {len(deleted_lines)} lines containing '{search_content}' from {dockerfile_path}")
    return True

if __name__ == "__main__":
    # Simple command line interface
    if len(sys.argv) < 3:
        print("Usage: python docker_line_deleter.py [dockerfile_path] [content_to_find] [--multiline]")
        print("  --multiline: optional flag to handle multiline instructions with backslash continuations")
        sys.exit(1)
    
    dockerfile_path = sys.argv[1]
    content_to_find = sys.argv[2]
    multiline = "--multiline" in sys.argv
    
    if not os.path.exists(dockerfile_path):
        print(f"Error: File {dockerfile_path} does not exist")
        sys.exit(1)
    
    delete_lines_from_dockerfile(dockerfile_path, content_to_find, multiline)