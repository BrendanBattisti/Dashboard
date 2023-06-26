import { useState, useEffect } from "react";
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
    }, 1000 * 60 * 60 * 24); // Refreshes reddit threads
    fetchData();

    

  }, []);

  function Item(data) {
    return <div>data</div>
  }


  return <div>
    data.map(Item)
  </div>




}