const fs = require("fs")
const AnyList = require("anylist");
var express = require("express");
var app = express();

const config = JSON.parse(fs.readFileSync("shoppingEnv.json"))

const any = new AnyList({
  email: config.email,
  password: config.password,
});

function getName(item) {
  return item._name;
}

async function updatedList() {
    await any.getLists();
    return any.getListByName(config.list).items;
}

async function getList() {
    list = await updatedList()
  return list.map(getName);
}

async function addItem(item) {
    list = await updatedList()

  let any_item = any.createItem(item);

  any_item = await list.addItem(any_item);

  await any_item.save();
}

async function deleteItem(item) {
    list = await updatedList()
    let any_item = any.createItem(item);

    list.removeItem(any_item)

    await any_item.save();
}

any.login().then(async () => {
    await any.getLists();
  
    var server = app.listen(config.port, function () {
        var host = server.address().address
        var port = server.address().port
        console.log("Example app listening at http://%s:%s", host, port)
     })
    
     app.get("/shopping", async function (req, res) {
        const result = await getList()
        res.json(result)
     })

     app.put('/shopping', async function (req, res) {

        console.log(req.params)
        console.log(req.body)

      })

      app.delete('/shopping', async function (req, res) {

        console.log(req.params)
        console.log(req.body)

      })
});
