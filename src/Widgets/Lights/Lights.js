import { useState } from "react";
import axios from "axios";
import { useEffect } from "react";
import styles from "./lights.module.css"

// Widget for monitoring and controlling the smart lights in the house
export default function Lights() {

    const [lightsData, setLights] = useState([])

    useEffect( () => {

        
        const fetchData = async () => {
            const response = await axios("/lights");
            setLights(response.data)
          };
      
          const interval = setInterval(() => {
            fetchData();
          }, 1000 * 60 * 1); // Refreshes the lights
          fetchData();

    }, [])

    async function ToggleLight(name, current_state) {

        const payload = {name: name, on: !current_state}

        const response = await axios.put("/lights", payload)

        setLights(response.data)
    }

    function LightSwitch(data) {
        return <div onClick={() => ToggleLight(data.name, data.on)}>{data.name}: {String(data.on)}</div>
    }

    return (<div className={styles.lights}><div>{lightsData.map(LightSwitch)}</div></div>)




}