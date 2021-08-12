function remove_input(input_name) {
    input_button = $(`input[name=${input_name}]`)[0].parentNode.parentNode;
    if (input_button.parentNode.childElementCount != 1)
        input_button.parentNode.removeChild(input_button);
    else
        $(`input[name=${input_name}]`)[0].value = ""
}
function add_input(position, name, value) {
    var text = set_input(name, value);
    var account_tag = document.getElementById(name);
    account_tag.insertAdjacentHTML(position, text);
}
function set_input(name, value) {
    let index;
    let content;
    if (name == "account") {
        index = account_index;
        content = "帳號 密碼"
        account_index += 1;
    }
    else if (name == "time") {
        index = time_index
        content = "時間"
        time_index += 1
    }
    input = `
    <div class="input_button">
    <div class="txt_field">
    <input type="text" name="${name + index}" value="${value}">
    <span class="underline"></span>
    <label>${content}</label>
    </div>
    <button type="button" class="remove_block" onclick="remove_input('${name + index}')"><span></span><span></span></div>
    </div>`
    return input;
}
var account_index = 0
var time_index = 0

add_input('beforeend', 'account', '', '帳號 密碼')
add_input('beforeend', 'time', '', '時間')

$.get('ajax/getSetting', function (data) {
    console.log(data);
    for (let i = data["time"].length - 1; i >= 0; i--) {
        console.log(data["time"][i])
        add_input('afterbegin', 'time', data["time"][i])
    }
    for (let i = data["accounts"].length - 1; i >= 0; i--) {
        console.log(data["accounts"][i])
        add_input('afterbegin', 'account', data["accounts"][i]["uid"] + " " + data["accounts"][i]["passwd"])
    }
});

$.get('ajax/getPort', function (data) {
    console.log(data)
    $(`input[name=port]`)[0].value = data
});