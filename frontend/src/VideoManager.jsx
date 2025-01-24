import { styled } from "@mui/material/styles";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import Button from "@mui/material/Button";
import ListSubheader from "@mui/material/ListSubheader";
import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import { ListItem } from "@mui/material";
import { useState, useEffect } from "react";
import CircularProgress from "@mui/material/CircularProgress";
import axios from "axios";
import DeleteIcon from "@mui/icons-material/Delete";
export function VideoManager({ videoList, serverConnection }) {
  const VisuallyHiddenInput = styled("input")({
    clip: "rect(0 0 0 0)",
    clipPath: "inset(50%)",
    height: 1,
    overflow: "hidden",
    position: "absolute",
    bottom: 0,
    left: 0,
    whiteSpace: "nowrap",
    width: 1,
  });
  const [isUploading, setIsUploading] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);
  const handleSubmit = (file) => {
    setIsUploading(true);
    const formdata = new FormData();
    formdata.append("file", file[0]);
    axios
      .post("http://localhost:8000/video/", formdata, {
        "Content-Type": "multipart/form-data",
      })
      .then((res) => setIsUploading(false));
  };

  const deleteFile = (filename) => {
    setIsDeleting(true);
    const f = filename.toString().replace(".mp4", "");
    axios
      .delete("http://localhost:8000/video/" + f)
      .then(() => setIsDeleting(false));
  };

  // useEffect(()=> {axios.get("http://localhost:8000/video/queue").then(res => console.log(res))}, [serverConnection])

  return (
    <>
      <div className="flex flex-col">
        <div className="flex flex-row items-center justify-start gap-4">
          <h2 className="font-bold text-2xl">Video Files: </h2>

          <Button
            component="label"
            role={undefined}
            variant="contained"
            tabIndex={-1}
            startIcon={<CloudUploadIcon />}
            disabled={isUploading || isDeleting}
            loading={isUploading}
          >
            Upload files
            <VisuallyHiddenInput
              type="file"
              onChange={(event) => handleSubmit(event.target.files)}
              multiple
            />
          </Button>
        </div>

        <List>
          {videoList.map((x) => (
            <ListItem>
              <ListItemText>{x}</ListItemText>
              <Button
                startIcon={<DeleteIcon />}
                onClick={() => deleteFile(x)}
                color="error"
                variant="contained"
                disabled={isDeleting}
                loading={isDeleting}
              >
                刪除
              </Button>
            </ListItem>
          ))}
        </List>
      </div>
    </>
  );
}
