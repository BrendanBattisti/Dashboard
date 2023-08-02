const fs = require("fs");
const AnyList = require("anylist");
var express = require("express");
const life360 = require("life360-node-api");
var app = express();
const bodyParser = require("body-parser");
app.use(bodyParser.json());

const config = JSON.parse(fs.readFileSync("nodeEnv.json"));

const any = new AnyList({
  email: config.shopping.email,
  password: config.shopping.password,
});

function getName(item) {
  return item._name;
}

async function updatedList() {
  await any.getLists();
  return any.getListByName(config.shopping.list);
}

async function getList() {
  list = await updatedList();
  return list.items.map(getName);
}

async function addItem(item) {
  list = await updatedList();

  let any_item = any.createItem({ name: item });

  any_item = await list.addItem(any_item);
  console.log(any_item);
  await any_item.save();
  return list.items.map(getName);
}

async function deleteItem(item) {
  list = await updatedList();
  let any_item = list.getItemByName(item);
  await list.removeItem(any_item);

  return list.items.map(getName);
}

// Login to Life360 and retrieve the client
const loginToLife360 = async () => {
  try {
    const client = await life360.login(
      config.life360.username,
      config.life360.password
    );
    return client;
  } catch (error) {
    console.error("Failed to login to Life360:", error);
    throw error;
  }
};

// Get a list of circles and log their names
const listCircles = async (client) => {
  try {
    const circles = await client.listCircles();
    return circles;
  } catch (error) {
    console.error("Failed to list circles:", error);
    throw error;
  }
};

// Get a list of members in a circle and log their names and locations
const listMembers = async (circle) => {
  try {
    const members = await circle.listMembers();
    for (const member of members) {
      //console.log(`${member.firstName} ${member.lastName}`);
      // console.log(`${member.location.latitude}, ${member.location.longitude}`);
    }
    return members;
  } catch (error) {
    console.error("Failed to list members:", error);
    throw error;
  }
};

any.login().then(async () => {
  await any.getLists();

  var server = app.listen(config.server.port, function () {
    var host = server.address().address;
    var port = server.address().port;
    console.log("Example app listening at http://%s:%s", host, port);
  });

  app.get("/shopping", async function (req, res) {
    const result = await getList();
    res.json(result);
  });

  app.put("/shopping", async function (req, res) {
    console.log(req.params);
    console.log(req.body);
  });

  app.delete("/shopping", async function (req, res) {
    const result = await deleteItem(req.body.item);
    res.json(result);
  });

  app.post("/shopping", async function (req, res) {
    const result = await addItem(req.body.item);
    res.json(result);
  });

  // Define the GET route for "/life360"
  app.get("/life360", async (req, res) => {
    try {
      const client = await loginToLife360();
      const circles = await listCircles(client);

      const familyInformation = [];

      for (const circle of circles) {
        if (circle.name.toLowerCase() == config.life360.circle.toLowerCase()) {
          let members = await circle.listMembers();

          for (const member of members) {
            console.log(`${member.firstName} ${member.lastName}`);
            console.log(
              `${member.location.latitude}, ${member.location.longitude}`
            );

            console.log(member.location.name);
          }
        }
      }
      //const members = await listMembers(myCircle);
      res.json(["Gay", "Frogs"]);
      //res.json({ circles });
    } catch (error) {
      console.error("Failed to fetch Life360 data:", error);
      res.status(500).json({ error: "Failed to fetch Life360 data" });
    }
  });
});
