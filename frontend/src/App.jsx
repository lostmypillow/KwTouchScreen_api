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
  const [count, setCount] = useState(0);
  const [serverConnection, setServerConnection] = useState(false);
  const [clientConnection, setClientConnection] = useState(false);
  const [ws, setWs] = useState(null); // Store the WebSocket object
  const [wsRefresh, setWsRefresh] = useState(false)

  // Function to initialize WebSocket
  const initializeWebSocket = () => {
    setWsRefresh(true)
    const ws = new WebSocket("ws://localhost:8000/ws/control");

    // On WebSocket open, set connection state to true
    ws.onopen = () => {
      console.log("WebSocket connected");
      setServerConnection(true);
    };

    // On WebSocket message, update server connection state
    ws.onmessage = (event) => {
      console.log("Message received: ", event.data);
      // You can update the state based on the received message if necessary
    };

    // On WebSocket error, set connection state to false
    ws.onerror = (error) => {
      console.error("WebSocket error: ", error);
      setServerConnection(false);
    };

    // On WebSocket close, set connection state to false
    ws.onclose = () => {
      console.log("WebSocket disconnected");
      setServerConnection(false);
    };

    // Set the WebSocket object in state
    setWs(ws);
    setWsRefresh(false)
  };

  // Initialize WebSocket on component mount
  useEffect(() => {
    initializeWebSocket(); // First connection attempt

    // Cleanup the WebSocket connection when the component is unmounted
    return () => {
      if (ws) {
        console.log("Cleaning up WebSocket connection");
        ws.close();
      }
    };
  }, []); // Empty dependency array ensures this runs once on mount

  // Handle button press to refresh the WebSocket connection
  const handleReconnect = () => {
    
    if (ws) {
      console.log("Closing existing WebSocket connection...");
      ws.close(); // Close the existing WebSocket
    }
    console.log("Reconnecting WebSocket...");
    initializeWebSocket(); // Reinitialize WebSocket connection
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
          <div className="flex flex-grow font-bold text-2xl">Dashboard</div>
        </Toolbar>
      </AppBar>

      <div className="flex flex-col items-start justify-start gap-4 p-8">
        <div className="flex flex-row items-center justify-between w-full">
          <h2 className="text-2xl">Server: {serverConnection ? "Connected" : "Disconnected"}</h2>

          <Button
          loading={wsRefresh}
            variant="contained"
            startIcon={<RefreshIcon />}
            onClick={handleReconnect}
          >
            Refresh
          </Button>
        </div>
        <VideoManager />
      </div>
    </>
  );
}

export default App;
