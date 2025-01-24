import { useState, useEffect } from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import Divider from "@mui/material/Divider";
import MenuIcon from "@mui/icons-material/Menu";
import StorageIcon from "@mui/icons-material/Storage";
import PhoneAndroidIcon from "@mui/icons-material/PhoneAndroid";
import { VideoManager } from "./VideoManager";
import RefreshIcon from "@mui/icons-material/Refresh";
function App() {
  const [serverConnection, setServerConnection] = useState(false);
  const [clientConnection, setClientConnection] = useState(false);
  const [wsState, setWsState] = useState(null);
  const [videoList, setVideoList] = useState([]);
  const [videoStatus, setVideoStatus] = useState("");

  const initWs = () => {
    const ws = new WebSocket("ws://localhost:8000/ws/control");
    setWsState(ws);

    // On WebSocket open, set connection state to true
    ws.onopen = () => {
      console.log("WebSocket connected");
      setServerConnection(true);
    };

    // On WebSocket message, update server connection state
    ws.onmessage = (event) => {
      console.log("Message received");
      const message = JSON.parse(event.data);
      if (message.action == "update queue") {
        setVideoList(message.message);
      } else if (message.action == "update client status") {
        message.message == "connected"
          ? setClientConnection(true)
          : setClientConnection(false);
      } else {
        console.log(message);
      }
    };

    // On WebSocket error, set connection state to false
    ws.onerror = (error) => {
      console.error("WebSocket error: ", error);
      setServerConnection(false);
      ws.close();
    };

    // On WebSocket close, set connection state to false and prepare for reconnection
    ws.onclose = () => {
      console.log("WebSocket disconnected");
      setServerConnection(false);
    };
    // Cleanup the WebSocket connection when the component is unmounted
    return () => ws.close();
  };
  // Initialize WebSocket on component mount
  useEffect(() => {
    initWs();
  }, []); // Empty dependency array ensures this runs once on mount

  // Handle button press to refresh the WebSocket connection
  const handleReconnect = () => {
    if (wsState != null) {
      wsState.close();
      setServerConnection(false);
    }
    initWs();
  };

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <div className="flex flex-grow font-bold text-3xl">Dashboard</div>
        </Toolbar>
      </AppBar>

      <div className="flex flex-col items-start justify-start gap-4 p-8">
        <div className="flex flex-row items-center justify-start gap-4 w-full">

          <h2 className="font-bold text-2xl">
            Server: {serverConnection ? "Connected" : "Disconnected"}
          </h2>
          <Button disabled={serverConnection} startIcon={<RefreshIcon />} variant="contained" onClick={handleReconnect}>Reconnect</Button>

        </div>
        <h2 className="font-bold text-2xl">
          Touchscreen: {clientConnection ? "Connected" : "Disconnected"}
        </h2>

        <VideoManager
          videoList={videoList}
          serverConnection={serverConnection}
        />
      </div>
    </>
  );
}

export default App;
