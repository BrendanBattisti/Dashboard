import { useEffect, useState } from "react";
import axios from "axios";
import styles from "./reddit.module.css";

// Module for showing trending reddit posts found on the popular page of reddit
export default function Reddit() {
  const [data, setData] = useState([]);
  const [active, setActive] = useState(2);

  useEffect(() => {
    const fetchData = async () => {
      const response = await axios("reddit");
      setData(response.data);
    };

    const interval = setInterval(() => {
      fetchData();
    }, 1000 * 60 * 24); // Refreshes reddit threads
    fetchData();
  }, []);

  function switchThread(new_state) {

    if ((new_state >= 0) && (new_state < data.length)) {
        setActive(new_state)
    } 
    
  }

  function Thread(thread, index) {
    return (
      <div className={index === active ? styles.container : styles.hidden } onClick={() => window.location.href = thread.link}>
        <div>
          <img className={styles.subRedditImage} src={thread.subreddit_img} />
          <div>{thread.title}</div>
        </div>
        <div>
          <div>{thread.upvotes}</div>
          <div>{thread.comments}</div>
        </div>
      </div>
    );
  }

  return <div>{data.map(Thread)}</div>;
}
