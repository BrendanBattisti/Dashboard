// Module for showing important calendar events that are happening or upcoming using the google calendar api
import { useState, useEffect } from "react";
import axios from "axios";
import capitalizeFirstLetter from "../../Util/utils";
import styles from "./calendar.module.css";
export default function Calendar() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    await axios
      .get("api/calendar")
      .then((data) => {
        setData(data.data);
      })
      .catch((error) => {
        console.log(error.response.status);
      });
  };

  function Event(data) {
    return (
      <div
        key={data.name}
        className={styles.event}
        onClick={() => window.open(data.link, "_blank")}
        style={{ color: data.color, cursor: "pointer" }}
      >
        {capitalizeFirstLetter(data.name)}
      </div>
    );
  }

  function Split(data) {
    if (data[1][0].length > 0) {
      return (
        <div key={data[1][1]}>
          {capitalizeFirstLetter(data[1][1])}

          {data[1][0].map(Event)}
        </div>
      );
    }
  }

  return <div>{Object.entries(data).map(Split)}</div>;
}
