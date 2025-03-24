import os
import sys
import tempfile
import subprocess
import shutil

def convert_ppt_to_pptx(ppt_path):
    """Convert .ppt to .pptx using available tools."""
    # Create temp file with unique name
    temp_dir = tempfile.gettempdir()
    temp_filename = f"temp_{os.path.basename(ppt_path).rsplit('.', 1)[0]}_{os.urandom(4).hex()}.pptx"
    pptx_path = os.path.join(temp_dir, temp_filename)
    
    manual_conversion_msg = """
No conversion tools found. You have these options:
1. Manually convert the .ppt file to .pptx:
   - Open the file in Microsoft PowerPoint, LibreOffice, or WPS Office
   - Save As -> Select .pptx format
   - Try again with the converted file
2. Install one of these tools:
   - LibreOffice (Recommended): Install from your system's package manager
   - unoserver: pip install unoserver (requires LibreOffice)
   - unoconv: Available in package manager (requires LibreOffice)
"""
    try:
        if sys.platform == 'win32':
            try:
                print("Attempting conversion using Microsoft PowerPoint...")
                import win32com.client
                powerpoint = win32com.client.Dispatch("PowerPoint.Application")
                powerpoint.Visible = False
                deck = powerpoint.Presentations.Open(ppt_path)
                deck.SaveAs(pptx_path, 24)  # 24 = .pptx format
                deck.Close()
                powerpoint.Quit()
                print("Successfully converted using Microsoft PowerPoint")
                return pptx_path
            except Exception as e:
                raise IOError(f"PowerPoint automation failed: {e}\n{manual_conversion_msg}")
        else:
            # conversion tools in order of preference
            converters = [
                {
                    'name': 'unoserver',
                    'cmd': ['unoconvert', ppt_path, pptx_path],
                    'install': 'pip install unoserver (requires LibreOffice)'
                },
                {
                    'name': 'unoconv',
                    'cmd': ['unoconv', '-f', 'pptx', '-o', pptx_path, ppt_path],
                    'install': 'Install from package manager (requires LibreOffice)'
                },
                {
                    'name': 'soffice',
                    'cmd': ['soffice', '--headless', '--convert-to', 'pptx', '--outdir', temp_dir, ppt_path],
                    'post_process': lambda: os.path.join(temp_dir, os.path.basename(ppt_path).rsplit('.', 1)[0] + '.pptx'),
                    'install': 'Install LibreOffice'
                }
            ]
            errors = []
            for converter in converters:
                if shutil.which(converter['cmd'][0]):  # Check if command exists
                    try:
                        print(f"Attempting conversion using {converter['name']}...")
                        result = subprocess.run(
                            converter['cmd'],
                            capture_output=True,
                            text=True
                        )
                        
                        # Check if soffice (which uses a different output path convention)
                        if converter['name'] == 'soffice' and result.returncode == 0:
                            soffice_output = converter['post_process']()
                            if os.path.exists(soffice_output):
                                # Copy to expected path
                                shutil.copy2(soffice_output, pptx_path)
                                print(f"Successfully converted using {converter['name']}")
                                return pptx_path
                        
                        # For other converters
                        elif result.returncode == 0 and os.path.exists(pptx_path):
                            print(f"Successfully converted using {converter['name']}")
                            return pptx_path
                        else:
                            errors.append(f"{converter['name']}: Command failed with return code {result.returncode}")
                    except Exception as e:
                        errors.append(f"{converter['name']}: {str(e)}")
                        print(f"Failed to convert using {converter['name']}")
                        continue
                else:
                    print(f"{converter['name']} not found, trying next method...")
            # no converter worked
            error_msg = "\n".join([
                "Failed to convert .ppt to .pptx automatically.",
                manual_conversion_msg,
                "\nTechnical details:",
                *errors
            ])
            raise IOError(error_msg)
    except Exception as e:
        raise e
