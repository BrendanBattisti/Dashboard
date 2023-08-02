import React, { useState, useEffect } from "react";
import {
  Container,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  TextField,
  Button,
} from "@mui/material";
import axios from "axios";

export default function ShoppingList() {
  const [data, setData] = useState([]);
  const [newItem, setNewItem] = useState("");

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const response = await axios.get("api/shopping");
    setData(response.data);
  };

  const handleAddItem = async () => {
    if (newItem.trim() !== "") {
      // Assuming the API endpoint supports adding new items
      const response = await axios.post("api/shopping", { item: newItem });
      setData(response.data);
    }
  };

  const handleDeleteItem = async (item) => {
    // Assuming the API endpoint supports deleting items by ID
    const response = await axios.delete(`api/shopping/${item}`);
    setData(response.data);
  };

  return (
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
                <span class="material-symbols-outlined">delete</span>
              </IconButton>
            </ListItemSecondaryAction>
          </ListItem>
        ))}
      </List>
      <TextField
        label="Add New Item"
        variant="outlined"
        fullWidth
        value={newItem}
        onChange={(e) => setNewItem(e.target.value)}
        margin="normal"
      />
      <Button variant="contained" color="primary" onClick={handleAddItem}>
        Add
      </Button>
    </Container>
  );
}
