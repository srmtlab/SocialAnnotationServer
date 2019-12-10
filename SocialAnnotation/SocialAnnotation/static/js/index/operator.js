function data_formatting(status, operation, data) {
    return {
        "status" : status,
        "operation" : operation,
        "data" : data
    }
}
/* start add node */
function show_add_node() {
    $('#add-node').modal();
}

function send_add_node() {

    let node_form = document.addNode;
    if(node_form.checkValidity() === false){
        node_form.classList.add("was-validated");
        return;
    }

    let node_name = document.getElementById("add-node-name").value.trim();
    let node_type = document.getElementById("add-node-type").value;
    let node_description = document.getElementById("add-node-description").value.trim();

    let json_data = {
        'hypothesis_url' : node_name,
        "annotation_type": node_type,
        'relevant_url' : node_description
    };
    let add_data = data_formatting("work","add",json_data);
    connection.send(JSON.stringify(add_data));

    $('#add-node').modal('hide');
    modal_obj = undefined;
}

function add_node(data) {
    annotation_list.unshift(data)
}
/* end add node */

/* start delete node */
function show_delete_node(annotation) {
    modal_obj = annotation;

    $("#delete-modal-body").html("アノテーション : <span style=\"color:red\">" + annotation.hypothesis_text + "</span>&nbspを削除しますか？");
    $('#delete-node').modal();
}

function send_delete_node(d) {

    let json_data = {
        'annotation_id' : d.annotation_id
    };
    let delete_data = data_formatting("work","delete", json_data);
    connection.send(JSON.stringify(delete_data));
    modal_obj = undefined;
}
function delete_node(data) {

    annotation_list.some(function (v, i) {
          if(v['annotation_id']===data['annotation_id']){
              annotation_list.splice(i,1);
          }
      }  
    );
}
/* end delete node */

/* start edit node */
function show_edit_node(annotation) {
    modal_obj = annotation;

    document.getElementById("edit-node-name").value = annotation.hypothesis_url;
    document.getElementById("edit-node-text").value = annotation.hypothesis_text;
    document.getElementById("edit-node-type").value = annotation.annotation_type;
    document.getElementById("edit-node-description").value = annotation.relevant_url;

    $('#edit-node').modal();

}

function send_edit_node(d) {

    let node_form = document.editNode;
    if(node_form.checkValidity() === false){
        node_form.classList.add("was-validated");
        return;
    }

    let node_type = document.getElementById("edit-node-type").value;
    let node_description = document.getElementById("edit-node-description").value.trim();

    let json_data = {
        'annotation_id' : d.annotation_id,
        "annotation_type": node_type,
        'relevant_url' : node_description
    };
    let edit_data = data_formatting('work','edit', json_data);
    connection.send(JSON.stringify(edit_data));

    $('#edit-node').modal('hide');
    modal_obj = undefined;
}

function edit_node(data) {
    annotation_list.some(function (v, i) {
          if(v['annotation_id']===data['annotation_id']){
              v['annotation_type'] = data['annotation_type'];
              v['relevant_url'] = data['relevant_url'];
          }
      }
    );
}
/* end edit node */