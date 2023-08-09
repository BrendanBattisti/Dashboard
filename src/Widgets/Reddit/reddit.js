import { useEffect, useState } from "react";
import axios from "axios";
import styles from "./reddit.module.css";

// Module for showing trending reddit posts found on the popular page of reddit
export default function Reddit() {
  const [data, setData] = useState([]);
  const [active, setActive] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      await axios("api/reddit")
        .then((data) => {
          setData(data.data);
        })
        .catch((error) => {
          console.log(error.response.status);
        });
    };

    const interval = setInterval(() => {
      fetchData();
    }, 1000 * 60 * 60 * 24); // Refreshes reddit threads
    fetchData();
  }, []);

  function switchThread(new_state) {
    if (new_state >= 0 && new_state < data.length) {
      setActive(new_state);
    } else if (new_state < 0) {
      setActive(data.length - 1);
    } else if (new_state >= data.length) {
      setActive(0);
    }
  }

  function Thread(thread, index) {
    return (
      <div className={index === active ? null : styles.hidden}>
        <div onClick={() => window.open(thread.link, "_blank")}>
          <div className={styles.row}>
            <img className={styles.subRedditImage} src={thread.subreddit_img} />
            <div>{thread.title}</div>
          </div>
          <div className={styles.numbers_row}>
            <div>{thread.upvotes}</div>
            <div>{thread.comments}</div>
          </div>
        </div>
        <div>
          <button onClick={() => switchThread(index - 1)}></button>
          <button onClick={() => switchThread(index + 1)}></button>
        </div>
      </div>
    );
  }
  if (data != null) {
    return <div className={styles.container}>{data.map(Thread)}</div>;
  } else {
  }
}
