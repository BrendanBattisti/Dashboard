import { useState } from "react";
import axios from "axios";
import { useEffect } from "react";
import styles from "./lights.module.css";
import { Switch } from "@mui/material";
import capitalizeFirstLetter from "../../Util/utils";
// Widget for monitoring and controlling the smart lights in the house
export default function Lights() {
  const [data, setData] = useState([]);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      await axios("api/lights")
        .then((data) => {
          setData(data.data);
        })
        .catch((error) => {
          console.log(error.response.status);
        });
    };

    setInterval(() => {
      fetchData();
    }, 1000 * 60 * 60 * 24); // Refreshes the lights
    fetchData();
  }, []);

  async function refreshLight() {
    await axios
      .put("api/lights")
      .then((data) => {
        setData(data.data);
      })
      .catch((error) => {
        console.log(error.response.status);
      });
  }

  async function ToggleLight(name, current_state) {
    const payload = { name: name, on: !current_state };

    await axios
      .put("api/lights", payload)
      .then((data) => {
        setData(data.data);
      })
      .catch((error) => {
        console.log(error.response.status);
      });
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

  const content = (
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
          onClick={() => refreshLight()}
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
  return data.length != 0 ? content : null;
}
