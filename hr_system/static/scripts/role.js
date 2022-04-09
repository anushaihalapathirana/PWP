const DEBUG = true;
const MASONJSON = "application/vnd.mason+json";
const PLAINJSON = "application/json";

function renderError(jqxhr) {
  let msg = jqxhr.responseJSON ? jqxhr.responseJSON["@error"]["@message"] : '';
  $("div.notification").html("<p class='error'>" + msg + "</p>");
}

function renderMsg(msg) {
  $("div.notification").html("<p class='msg'>" + msg + "</p>");
}

function getResource(href, renderer) {
  $.ajax({
    url: href,
    success: renderer,
    error: renderError,
  });
}

function sendData(href, method, item, postProcessor) {
  $.ajax({
    url: href,
    type: method,
    data: JSON.stringify(item),
    contentType: PLAINJSON,
    processData: false,
    success: postProcessor,
    error: renderError,
  });
}

function roleRow(item) {
  let link =
    "<a href='" +
    item["@controls"].self.href +
    "' onClick='followLink(event, this, renderRole)'>show</a>";

  return (
    "<tr><td>" +
    item.name +
    "</td><td>" +
    item.code +
    "</td><td>" +
    item.description +
    "</td><td>" +
    link +
    "</td></tr>"
  );
}

function appendRoleRow(body) {
  $(".resulttable tbody").append(roleRow(body));
}

function getSubmittedRole(data, status, jqxhr) {
  renderMsg("Successful");
  let href = jqxhr.getResponseHeader("Location");
  if (href) {
    getResource(href, appendRoleRow);
  }
}

function followLink(event, a, renderer) {
  event.preventDefault();
  //   console.log("this", a);
  getResource($(a).attr("href"), renderer);
}

function submitRole(event) {
  event.preventDefault();

  let data = {};
  let form = $("div.form form");
  data.name = $("input[name='name']").val();
  data.code = $("input[name='code']").val();
  data.description = $("input[name='description']").val();

  sendData(form.attr("action"), form.attr("method"), data, getSubmittedRole);
}

function renderRoleForm(ctrl, formtitle) {
  let form = $("<form class='add-role-form'>");
  let name = ctrl.schema.properties.name;
  let code = ctrl.schema.properties.code;
  let description = ctrl.schema.properties.description;

  form.attr("action", ctrl.href);
  form.attr("method", ctrl.method);
  form.submit(submitRole);
  form.append("<h2 class= 'title-one'>" + formtitle + "</h2>");

  form.append("<label>" + name.description + "</label>");
  form.append("<input type='text' name='name'>");
  form.append("<label>" + code.description + "</label>");
  form.append("<input type='text' name='code'>");
  form.append("<label>" + description.description + "</label>");
  form.append("<input type='text' name='description'>");

  ctrl.schema.required.forEach(function (property) {
    $("input[name='" + property + "']").attr("required", true);
  });
  form.append("<input type='submit' name='submit' value='Submit'>");
  $("div.form").html(form);
}

function renderRole(body) {
  $("div.navigation").html(
    "<a href='" +
      body["@controls"].collection.href +
      "' onClick='followLink(event, this, renderRoles)'>Collection</a>"
  );
  $(".resulttable thead").empty();
  $(".resulttable tbody").empty();
  renderRoleForm(body["@controls"].edit, "Edit Role");

  $("input[name='name']").val(body.name);
  $("input[name='code']").val(body.code);
  $("input[name='description']").val(body.description);

}


// function renderMeasurements(body) {
//   //   console.log("BODY", body);

//   $(".resulttable thead").html("<tr><th>Time</th><th>Value</th>");
//   let tbody = $(".resulttable tbody");
//   tbody.empty();

//   let next = "#";

//   if (body["@controls"]["next"]) {
//     next = body["@controls"]["next"].href;
//   }

//   let prev = "#";

//   if (body["@controls"]["prev"]) {
//     prev = body["@controls"]["prev"].href;
//   }

//     console.log(next, prev.this);

//   $("div.tablecontrols").html(
//     "<a href='" +
//       prev +
//       "' onClick='followLink(event, this, renderMeasurements)' class='previd'>Prev</a>" +
//       " | " +
//       "<a href='" +
//       next +
//       "' onClick='followLink(event, this, renderMeasurements)' class='nextid'>Next</a>"
//   );

//   if (prev === "#") {
//     // console.log("HIDE");
//     $(".previd").remove();
//   }

//   if (next === "#") {
//     $(".nextid").remove();
//   }
//   $(".form").empty();
//   body.items.forEach(function (item) {
//     tbody.append(measurementRow(item));
//   });
// }

// function measurementRow(item) {
//   return "<tr><td>" + item.time + "</td><td>" + item.value + "</td></tr>";
// }

function renderRoles(body) {
    // $("div.navigation").html(
    //     "<a href='" +
    //       body["@controls"]["hrsys:employee-all"] +
    //       "' onClick='followLink(event, this, renderRoles)'>Employee Collection</a>"
    //   );
  $("div.tablecontrols").empty();
  $(".resulttable thead").html(
    "<div><tr><th>Name</th><th>Code</th><th>Description</th><th>Actions</th></tr></div>"
  );
  let tbody = $(".resulttable tbody");
  tbody.empty();
  body.items.forEach(function (item) {
    tbody.append(roleRow(item));
  });
  renderRoleForm(body["@controls"]["hrsys:add-role"], "Add Role");
}

$(document).ready(function () {
  getResource("http://127.0.0.1:5000/api/roles/", renderRoles);
});
