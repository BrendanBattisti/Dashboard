import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import reportWebVitals from "./reportWebVitals";
import Title from "./Title/title";
import Clock from "./Widgets/Clock/Clock";
import Weather from "./Widgets/Weather/Weather";
import Life360 from "./Widgets/Life360/Life360";
import Lights from "./Widgets/Lights/Lights";
import Reddit from "./Widgets/Reddit/reddit";


const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <link
      rel="stylesheet"
      href="https://fonts.googleapis.com/css?family=Anton"
    ></link>
    <link
      rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
    />
    <div className="vertical_flex">
      <Clock />
      <Reddit />
      <Lights />
    </div>
    <Weather />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
