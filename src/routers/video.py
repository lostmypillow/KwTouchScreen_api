from fastapi import APIRouter, Response, File, UploadFile
from typing import Annotated
from smbclient import link, open_file, register_session, stat, listdir, mkdir, rmdir, scandir
import logging
from smbclient.path import isdir
router = APIRouter(
    prefix="/video",
    tags=["Video"],
)
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@router.get('/')
def get_video():
    register_session("192.168.2.36", username="exam", password="exam")

    smb_path = r"\\192.168.2.36\kwwebsite\kwad\vid2.mp4"
    try:
       with open_file(smb_path, mode="rb") as file:
            # Read the content of the file into bytes
            video_bytes = file.read()
       return Response(
            content=video_bytes,
            media_type="video/mp4",  # Set the correct MIME type for your video file
            headers={"Content-Disposition": f"attachment; filename={'meow.mp4'}"}
        )
    except Exception as e:
        print(f"Error accessing SMB share: {e}")
# @router.get('/dir')
# def list_dir():
#     register_session("192.168.2.36", username="exam", password="exam")
#     
    


@router.post('/upload')
async def upload_video(file: UploadFile):
    register_session("192.168.2.36", username="exam", password="exam")
    smb_path = r"\\192.168.2.36\kwwebsite\kwad\\" + file.filename
    directory = []

    with open_file(smb_path, mode="wb") as fd:
        fd.write(await file.read())
    for file_info in scandir(r"\\192.168.2.36\kwwebsite\kwad"):
        file_inode = file_info.inode()
        if file_info.is_file():
            directory.append({"name": file_info.name,"inode":file_inode})
           
        elif file_info.is_dir():
            log.info("Dir: %s %d", file_info.name, file_inode)
        else:
            log.info("Symlink: %s %d", file_info.name, file_inode)
    return directory