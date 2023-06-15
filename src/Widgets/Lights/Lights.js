import { useState } from "react";
import axios from "axios";
import { useEffect } from "react";
import styles from "./lights.module.css";
import { Switch } from "@mui/material";
import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  status: {
    danger: "#e53e3e",
  },
  palette: {
    primary: {
      main: "#0971f1",
      darker: "#053e85",
    },
    neutral: {
      main: "#64748B",
      contrastText: "#fff",
    },
  },
});

// Widget for monitoring and controlling the smart lights in the house
export default function Lights() {
  const [lightsData, setLights] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await axios("/lights");
      setLights(response.data);
    };

    const interval = setInterval(() => {
      fetchData();
    }, 1000 * 60 * 1); // Refreshes the lights
    fetchData();
  }, []);

  async function ToggleLight(name, current_state) {
    const payload = { name: name, on: !current_state };

    const response = await axios.put("/lights", payload);

    setLights(response.data);
  }

  function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

  function LightSwitch(data) {
    return (
      <div>
        <Switch
          checked={data.on}
          onClick={() => ToggleLight(data.name, data.on)}
          label="TESTING"
        />
        {capitalizeFirstLetter(data.name)}
      </div>
    );
  }

  function LightsList(data) {
    return <div className={styles.lights_list}>{data.map(LightSwitch)}</div>;
  }

  return (
    <div className={styles.lights}>
      <div>{LightsList(lightsData)}</div>
    </div>
  );
}
