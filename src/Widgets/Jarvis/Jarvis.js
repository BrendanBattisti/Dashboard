import { useState } from "react";
import styles from "./jarvis.module.css";

export default function Jarvis() {
  const [active, setActive] = useState(true);
  const size = 20;
  function get_size(add) {
    return size + add + "vh";
  }

  const center = (
    <div
      onClick={() => setActive(!active)}
      className={styles.jarvis}
      style={{ width: get_size(0), height: get_size(0) }}
    ></div>
  );
  const borderColor = () => {
    return Math.random() > 0.45 ? "rgba(0, 238, 255, .7)" : null;
  };

  function Edge(contents, size) {
    if (size === 0) {
      return contents;
    }
    return (
      <div
        className={styles.edge}
        style={{
          width: get_size(size),
          height: get_size(size),
          animationIterationCount: active ? "infinite" : 0,
          animationDuration: `${Math.max(Math.round(Math.random() * 20), 10)}s`,
          animationDirection: Math.random() > 0.5 ? "reverse" : "normal",
          borderWidth: `${Math.max(Math.random() * 10, 3)}px`,
          borderTopColor: borderColor(),
          borderRightColor: borderColor(),
          borderBottomColor: borderColor(),
          borderLeftColor: borderColor(),
        }}
      >
        {Edge(contents, size - 2)}
      </div>
    );
  }
  return Edge(center, 14);
}
