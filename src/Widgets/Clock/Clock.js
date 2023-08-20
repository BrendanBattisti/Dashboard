import { useState, useEffect } from "react";
import styles from "./clock.module.css";
export default function Clock() {
  const [time, setDate] = useState(new Date());
  useEffect(() => {
    setInterval(checkTime, 1000);
  }, []);
  function formatTime(x) {
    if (x < 10) {
      x = "0" + x;
    }
    return x;
  }

  function ampm() {
    return time.getHours() > 12 ? "PM" : "AM";
  }

  function hours() {
    return time.getHours() >= 12 ? time.getHours() - 12 : time.getHours();
  }

  function checkTime() {
    setDate(new Date());
  }
  return (
    <div className={styles.clock}>
      <div className={styles.clock_text}>
        {hours()}:{formatTime(time.getMinutes())}:
        {formatTime(time.getSeconds())}
        {ampm()}
      </div>
      <div className={styles.clock_text}>
        {time.getMonth()}/{time.getDate()}/{time.getFullYear()}
      </div>
    </div>
  );
}
