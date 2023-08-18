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
          animation: `standard_rotation ${
            Math.random() * 20
          }s infinite reverse`,
        }}
      >
        {Edge(contents, size - 2)}
      </div>
    );
  }
  return Edge(center, 10);
}
