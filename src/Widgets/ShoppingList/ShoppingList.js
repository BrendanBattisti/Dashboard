import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import styles from "./ShoppingList.module.css";
export default function ShoppingList() {
  const [data, setData] = useState([]);
  const [newItem, setNewItem] = useState("");
  const containerRef = useRef();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const response = await axios
      .get("api/shopping")
      .then((data) => {
        setData(data.data);
      })
      .catch((error) => {
        console.log(error.response.status);
      });
  };

  const handleAddItem = async () => {
    if (newItem.trim() !== "") {
      // Assuming the API endpoint supports adding new items
      const response = await axios.post("api/shopping", { item: newItem });
      setData(response.data);
      setNewItem(""); // Clear the newItem state after adding the item
    }
  };

  const handleDeleteItem = async (name) => {
    // Assuming the API endpoint supports deleting items by ID
    const response = await axios.delete(`api/shopping/${name}`);
    setData(response.data);
  };

  return (
    <div className={styles.container}>
      <div className={styles.itemContainer}>
        {data.map((item, index) => (
          <div
            key={index}
            className={index % 2 == 0 ? styles.darkitem : styles.lightitem}
          >
            {item}
            <button
              className={styles.deleteButton}
              onClick={() => handleDeleteItem(item)}
            >
              <span
                className="material-symbols-outlined"
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
                delete
              </span>
            </button>
          </div>
        ))}
      </div>
      <div className={styles.controlInput}>
        <input
          type="text"
          placeholder="Enter new item"
          value={newItem}
          onChange={(e) => setNewItem(e.target.value)}
          className={styles.itemInput}
        ></input>
        <button onClick={handleAddItem}>
          <span
            className="material-symbols-outlined"
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
            add
          </span>
        </button>
      </div>
    </div>
  );
  return data.length != 0 ? content : null;
}
