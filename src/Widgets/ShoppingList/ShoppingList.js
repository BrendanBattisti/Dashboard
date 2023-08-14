import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

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

  const content = (
    <Container maxWidth="sm">
      <List>
        {data.map((item) => (
          <ListItem>
            <ListItemText primary={item} />
            <ListItemSecondaryAction>
              <IconButton
                edge="end"
                aria-label="delete"
                onClick={() => handleDeleteItem(item)}
              >
                delete
              </span>
            </button>
          </div>
        ))}
      </div>
      <div
        style={{
          position: "absolute",
          bottom: "0", // Anchor the input field and button to the bottom
          width: "100%", // Expand to the full width of the container
          borderTop: "1px solid rgba(0, 255, 255, 0.6)", // Add a top border
          boxSizing: "border-box", // Include border in the height calculation
          display: "flex", // Display the input field and button in a row
          alignItems: "center", // Align items vertically
          padding: "0 8px", // Add padding to the row (left and right)
        }}
      >
        <input
          type="text"
          placeholder="Enter new item"
          value={newItem}
          onChange={(e) => setNewItem(e.target.value)}
          style={{
            flex: "1", // Take up remaining space in the row
            border: "none", // Remove border
            borderBottom: "1px solid rgba(0, 255, 255, 0.6)", // Add a bottom border
            background: "transparent", // Transparent background
            color: "rgba(0, 255, 255, 0.8)", // Brighter cyan text color
            fontFamily: "Arial, sans-serif",
            fontWeight: "300",
            textShadow: "0 0 2px rgba(0, 255, 255, 0.8)", // Faint glow for text
            padding: "5px 0", // Add padding inside the input field (top and bottom)
            outline: "none", // Remove the default outline when the input is clicked
          }}
        />
        <button
          onClick={handleAddItem}
          style={{
            border: "none", // Remove border
            background: "transparent", // Transparent background
            color: "rgba(0, 255, 255, 0.8)", // Brighter cyan text color
            cursor: "pointer",
            fontSize: "18px",
            display: "flex",
            alignItems: "center",
          }}
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
            add
          </span>
        </button>
      </div>
    </div>
  );
  return data.length != 0 ? content : null;
}
