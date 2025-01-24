import smbclient as smb
import os
SMB_SERVER='192.168.1.102'
SMB_USERNAME='smbuser'
SMB_PASSWORD='Olgakempinnen0609'
smb_dir = f"\\\\{SMB_SERVER}\\kwwebsite\\kwad"
smb_session = smb.register_session(SMB_SERVER, username=SMB_USERNAME, password=SMB_PASSWORD) 
print([
        file.smb_info._asdict()
        for file in smb.scandir(smb_dir)
        if file.name.endswith('.mp4')
    ])