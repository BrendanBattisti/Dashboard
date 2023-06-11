import { useState } from "react";
import styles from "./weather.module.css";

export default function Day(weather) {
    const weekdays = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"];

    const [expanded, setExpanded] = useState(false)

    //const onClick = () => setExpanded(!expanded)
    const high = Math.round(weather.high);
    const low = Math.round(weather.low);

    const weather_type = weather.weather;
    const day = weather.weekday;
    return (
        <div className={styles.chunk} >
            <div>{weekdays[day]}</div>
            <div className={styles.temp}>
                H: {high}&deg; L: {low}&deg;
            </div>
            <div>
                <span className="material-symbols-outlined">{weather_type}</span>
            </div>

        </div>
    );
    //{expanded ? <div>GAY</div> : null}
}