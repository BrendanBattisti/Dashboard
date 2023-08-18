import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import reportWebVitals from "./reportWebVitals";
import Clock from "./Widgets/Clock/Clock";
import Weather from "./Widgets/Weather/Weather";
import Calendar from "./Widgets/Calendar/Calendar";
import Lights from "./Widgets/Lights/Lights";
import Reddit from "./Widgets/Reddit/reddit";
import ShoppingList from "./Widgets/ShoppingList/ShoppingList";

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
    <div className="horizontal_flex">
      <div className="vertical_flex">
        <Clock />
        <></> <Weather />
      </div>
      <div className="vertical_flex">
        <Calendar />
        <></>
        <ShoppingList />
      </div>
      <div className="vertical_flex">
        <Lights />
        <Reddit />
      </div>
    </div>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
