import { useState } from "react";
import axios from "axios";
import { useEffect } from "react";
import styles from "./lights.module.css";
import { Switch, TextField, Button } from "@mui/material";
import { createTheme } from "@mui/material/styles";

// Widget for monitoring and controlling the smart lights in the house
export default function Lights() {
  const [data, setData] = useState([]);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      const response = await axios("api/lights");
      setData(response.data);
    };

    const interval = setInterval(() => {
      fetchData();
    }, 1000 * 60 * 60 * 24); // Refreshes the lights
    fetchData();
  }, []);

  async function ToggleLight(name, current_state) {
    const payload = { name: name, on: !current_state };

    const response = await axios.put("api/lights", payload);

    setData(response.data);
  }

  function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

  function LightSwitch(data) {
    return (
      <div key={data.name}>
        <Switch
          checked={data.on}
          onClick={() => ToggleLight(data.name, data.on)}
        />
        {capitalizeFirstLetter(data.name)}
      </div>
    );
  }

  return (
    <div className={styles.lights}>
      <div className={styles.lights_list}>
        {data
          .filter((element) => {
            if (filter === "") {
              return element;
            } else if (
              element.name.toLowerCase().includes(filter.toLowerCase())
            ) {
              return element;
            }
          })
          .map(LightSwitch)}
      </div>
      <div className={styles.controlBlock}>
        <input
          id="search"
          label="Search"
          key="searchbar"
          onChange={(event) => setFilter(event.target.value)}
        />
        <div className={styles.buttonContainer}>
          <Button variant="contained" className="material-symbols-outlined">
            refresh
          </Button>
        </div>
      </div>
    </div>
  );
}
