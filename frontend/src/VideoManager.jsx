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
export function VideoManager() {
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
  const [videoList, setVideoList] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const getVideoList = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get("http://localhost:8000/video/sync");
      console.log(response);
    } catch (error) {
      console.error(error);
    }
    setIsLoading(false);
  };

  useEffect(() => {
    getVideoList();
  }, []);

  return (
    <>
      <div className="flex flex-col w-full">
        <div className="flex flex-row w-full items-center justify-between">
          <h2 className="font-semibold text-2xl">Video Files</h2>

          <Button
            component="label"
            role={undefined}
            variant="contained"
            tabIndex={-1}
            startIcon={<CloudUploadIcon />}
          >
            Upload files
            <VisuallyHiddenInput
              type="file"
              onChange={(event) => console.log(event.target.files)}
              multiple
            />
          </Button>
        </div>

        <List>
          {isLoading ? (
            <>
              {" "}
              <div className="flex flex-row items-center justify-start gap-4">
                {" "}
                <CircularProgress size="1rem" />
                <p>Loading files from server...</p>{" "}
              </div>
            </>
          ) : (
            ""
          )}
          {videoList.map((x) => (
            <ListItem>{x}</ListItem>
          ))}
        </List>
      </div>
    </>
  );
}
