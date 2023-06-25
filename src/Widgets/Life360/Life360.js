// Life 360 module for tracking the location of family members
import axios from "axios"
import { useEffect, useState } from "react";
import styles from "./life360.module.css";

export default function Life360() {


    const [data, setData] = useState();

    useEffect(() => {
        const fetchData = async () => {
          const response = await axios("api/life360");
          setData(response.data)
        };
    
        const interval = setInterval(() => {
          fetchData();
        }, 1000 * 60 * 24); // Refreshes the status
        fetchData();
    
      }, []);


      return (<div className={styles.container}>
        {data}
      </div>)
}