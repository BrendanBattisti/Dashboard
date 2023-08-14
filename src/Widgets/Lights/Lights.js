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

  function LightSwitch(data, index) {
    return (
      <div
        key={index}
        className={index % 2 == 0 ? styles.darkitem : styles.lightitem}
      >
        {capitalizeFirstLetter(data.name)}
        <Switch
          checked={data.on}
          onClick={() => ToggleLight(data.name, data.on)}
        />
      </div>
    );
  }

  const old = (
    <div className={styles.container}>
      <div className={styles.itemContainer}>
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
      <div className={styles.controlInput}>
        <input
          id="search"
          label="Search"
          key="searchbar"
          placeholder="Search"
          onChange={(event) => setFilter(event.target.value)}
          className={styles.itemInput}
        />
        <button
          variant="contained"
          className="material-symbols-outlined"
          style={{
            transition: "text-shadow 0.3s ease-in-out", // Apply transition to the text-shadow property
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.textShadow = "0 0 6px rgba(0, 255, 255, 0.8)"; // Faint glow on hover
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.textShadow = "none"; // Remove the glow when not hovering
          }}
        >
          refresh
        </button>
      </div>
    </div>
  );
  return old;
  const lights = (
    <div className={styles.container}>
      <div className={styles.itemContainer}>
        {data.map((item, index) => (
          <div
            key={index}
            className={index % 2 == 0 ? styles.darkitem : styles.lightitem}
          >
            {item}
            <button className={styles.deleteButton}>
              <span
                className="material-symbols-outlined"
                style={{
                  transition: "text-shadow 0.3s ease-in-out", // Apply transition to the text-shadow property
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.textShadow =
                    "0 0 6px rgba(0, 255, 255, 0.8)"; // Faint glow on hover
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.textShadow = "none"; // Remove the glow when not hovering
                }}
              >
                delete
              </span>
            </button>
          </div>
        ))}
      </div>
      <div className={styles.controlInput}>
        <input
          id="search"
          label="Search"
          key="searchbar"
          onChange={(event) => setFilter(event.target.value)}
        />
        <button>
          <span
            className="material-symbols-outlined"
            style={{
              transition: "text-shadow 0.3s ease-in-out", // Apply transition to the text-shadow property
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.textShadow =
                "0 0 6px rgba(0, 255, 255, 0.8)"; // Faint glow on hover
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.textShadow = "none"; // Remove the glow when not hovering
            }}
          >
            add
          </span>
        </button>
      </div>
    </div>
  );
}
