import { useState, useEffect } from "react";
import styles from "./shoppingList.module.css";
import axios from "axios";

export default function ShoppingList() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await axios("api/shopping");
      setData(response.data);
    };

    const interval = setInterval(() => {
      fetchData();
    }, 1000 * 60 * 60); // Refreshes reddit threads
    fetchData();
  }, []);

  function Item(data) {
    return <div>{data}</div>;
  }

  return <div className={styles.listContainer}>{data.map(Item)}</div>;
}
