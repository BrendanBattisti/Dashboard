import { useEffect, useState } from "react";
import styles from "./weather.module.css";
import axios from "axios";

export default function Weather() {
  const [weatherData, setWeatherData] = useState([]);

  const weekdays = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"];
  useEffect(() => {
    const fetchData = async () => {
      const response = await axios("weather");
      let data = response.data.map(Day);
      setWeatherData(data);
    };
    const interval = setInterval(() => {
      fetchData();
    }, 1000 * 60 * 24); // Refreshes the weather ever day
    fetchData();
  }, []);

  function Day(weather) {
    const high = Math.round(weather.high);
    const low = Math.round(weather.low);

    const weather_type = weather.weather;
    const day = weather.weekday;
    return (
      <div className={styles.chunk}>
        <div>{weekdays[day]}</div>
        <div className={styles.temp}>
          H: {high}&deg; L: {low}&deg;
        </div>
        <div>
          <span className="material-symbols-outlined">{weather_type}</span>
        </div>
      </div>
    );
  }

  // Add humidity to each weather chunk
  return (
    <div className={styles.weather}>
      <div className={styles.stream}>{weatherData}</div>
    </div>
  );
}
