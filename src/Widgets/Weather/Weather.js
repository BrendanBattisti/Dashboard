import { useEffect, useState } from "react";
import styles from "./weather.module.css";
import axios from "axios";

export default function Weather() {
  const [weatherData, setWeatherData] = useState([]);
  const [visible, setVisibile] = useState([])

  const weekdays = ["Mon", "Tue", "Wed", "Thur", "Fkri", "Sat", "Sun"];
  useEffect(() => {
    const fetchData = async () => {
      const response = await axios("weather");
      let data = response.data.map(Day);
      setWeatherData(data);

      if (visible.length === 0) {
        const length = data.length
        setVisibile(Array.from({ length }, () => false))
      }
    };
    const interval = setInterval(() => {
      fetchData();
    }, 1000 * 60 * 1); // Refreshes the weather
    fetchData();
  }, [visible]);

  function Hour(weather) {

    //const onClick = () => setVisible(!visible)

    //return (<div onClick={onClick}>Hello there</div>)
  }

  function Day(weather) {
    const index = weather.index

    const onClick = () => {
      const tmpVisible = visible
      tmpVisible[index] = !tmpVisible[index]
      setVisibile(tmpVisible)
      console.log(visible)
    }

    const high = Math.round(weather.high);
    const low = Math.round(weather.low);

    const weather_type = weather.weather;
    const day = weather.weekday;
    return (
      <div key={index}>
        <div className={styles.chunk} onClick={onClick}>
          <div>{weekdays[day]}</div>
          <div className={styles.temp}>
            H: {high}&deg; L: {low}&deg; {visible[index] ? "Penis" : null}
          </div>
          <div>
            <span className="material-symbols-outlined">{weather_type}</span>
          </div>

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
