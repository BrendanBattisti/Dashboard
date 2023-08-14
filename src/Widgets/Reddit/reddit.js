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
          if (data.data) {
            setData(data.data);
          }
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
      <div className={index === active ? styles.container : styles.hidden}>
        <div className={styles.row}>
          <img className={styles.subRedditImage} src={thread.subreddit_img} />
          <div
            onClick={() => window.open(thread.link, "_blank")}
            className={styles.title}
          >
            {thread.title}
          </div>
        </div>
        <div className={styles.numbers_row}>
          <button
            onClick={() => switchThread(index - 1)}
            style={{
              transition: "text-shadow 0.3s ease-in-out", // Apply transition to the text-shadow property
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.textShadow =
                "0 0 6px rgba(0, 255, 255, 0.8)"; // Faint glow on hover
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.textShadow = "none"; // Remove the glow when not hovering
            }}
          >
            <span className="material-symbols-outlined">arrow_back</span>
          </button>
          <div>
            <span className="material-symbols-outlined">thumb_up</span>
            {thread.upvotes}
          </div>
          <div>
            <span className="material-symbols-outlined">comment</span>
            {thread.comments}
          </div>
          <button
            onClick={() => switchThread(index + 1)}
            style={{
              transition: "text-shadow 0.3s ease-in-out", // Apply transition to the text-shadow property
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.textShadow =
                "0 0 6px rgba(0, 255, 255, 0.8)"; // Faint glow on hover
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.textShadow = "none"; // Remove the glow when not hovering
            }}
          >
            <span className="material-symbols-outlined">arrow_forward</span>
          </button>
        </div>
      </div>
    );
  }
  const content = <div>{data.map(Thread)}</div>;
  return data.length === 0 ? null : content;
}
