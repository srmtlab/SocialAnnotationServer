let init_flag = true;
let annotation_list = null;
let modal_obj = undefined;

function init_data(websocket_url){
    connection = new WebSocket(websocket_url);

    connection.onopen = function (e) {
        connection.send(JSON.stringify({
            'status': 'init'
        }));
    };

    connection.onmessage = function (e) {
        let receive_data = JSON.parse(e.data);
        let status = receive_data["status"];

        if(init_flag && status === "init"){
            annotation_list = receive_data["data"];

            new Vue({
                el: '#annotation-table',
                delimiters: ['${', '}'],
                data: {
                    current_annotation: null,
                    annotation_list : annotation_list,
                },
                methods:{
                    show_edit_annotation :function(annotation){
                        show_edit_node(annotation)
                    },
                    show_delete_annotation : function(annotation){
                        show_delete_node(annotation)
                    }
                }
            });

            init_flag = false;
        }
        else if(status === "work"){
            let operation = receive_data["operation"];
            let data = receive_data["data"];

            if(operation === "add"){
                add_node(data);
            }
            else if(operation === "delete"){
                delete_node(data);
            }
            else if(operation === "edit"){
                edit_node(data);
            }
        }
    };
}

window.onload = function () {
    let websocket_url = "ws://" + location.host + "/ws/";
    init_data(websocket_url);

    $("#add-node").on('hidden.bs.modal', function () {
        document.getElementById("add-node-name").value = "";
        document.getElementById("add-node-type").value = "";
        document.getElementById("add-node-description").value = "";
        document.addNode.classList.remove("was-validated");
    });

    $("#edit-node").on('hidden.bs.modal', function () {
        document.editNode.classList.remove("was-validated");
    });
};