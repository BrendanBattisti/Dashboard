import { useEffect, useState } from "react";
import styles from "./weather.module.css";
import axios from "axios";
import { Collapse } from "@mui/material";

export default function Weather() {
  const [data, setData] = useState([]);
  const [active, setActive] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      await axios("api/weather")
        .then((data) => {
          setData(data.data);
        })
        .catch((error) => {
          console.log(error.response.status);
        });
    };

    setInterval(() => {
      fetchData();
    }, 1000 * 60 * 60 * 12); // Refreshes the weather
    fetchData();
  }, []);

  function Hour(weather) {
    let time = new Date(weather.dt * 1000).getHours();

    time = (time > 12 ? time - 12 : time) + (time > 12 ? "PM" : "AM");

    return (
      <div className={styles.hour}>
        <div>{Math.round(weather.temp)}</div>
        <span className="material-symbols-outlined">{weather.weather}</span>
        <div>{time}</div>
      </div>
    );
  }

  function Day(weather) {
    const index = weather.index;

    const onClick = () => {
      if (active === index) {
        setActive(-1);
      } else {
        setActive(index);
      }
    };

    return (
      <div key={weather.index}>
        <div className={styles.chunk} onClick={onClick}>
          <div>{weather.weekday}</div>
          <div className={styles.temp}>
            H: {Math.round(weather.high)}&deg; L: {Math.round(weather.low)}&deg;
          </div>
          <span className="material-symbols-outlined">{weather.weather}</span>
        </div>
        <Collapse in={active === index}>
          <div className={styles.hourly}>{weather.chunks.map(Hour)}</div>
        </Collapse>
      </div>
    );
  }

  // Add humidity to each weather chunk
  return (
    <div className={styles.weather}>
      <div className={styles.stream}>{data.map(Day)}</div>
    </div>
  );
}
