
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
    input = `<label class="form-group">
    <input type="text" class="form-control" name="${name + index}" value="${value}">
    <span>${content}</span>
    <span class="border"></span>
    </label>`
    return input;
}
// var account_index = 0
// var time_index = 0

// add_input('beforeend', 'account', '', '帳號 密碼')
// add_input('beforeend', 'time', '', '時間')

$.get('ajax/getStatus', function (data) {
    for (let account in data) {
        let insert_text = `<div class="status">${account}:<br>`
        if (data[account]["login"] == 1) {
            // console.log("登入成功")
            insert_text += "&emsp;✔️登入成功<br>"
            if (data[account]["status"]["signin"] == 1) {
                insert_text += `&emsp;✔️今日已簽到<br>`
                // console.log("今日已簽到")
            } 
            else if (data[account]["status"]["signin"] == 0) {
                insert_text += `&emsp;❌今日未簽到<br>`
                // console.log("今日未簽到")
            }
            insert_text+=`&emsp;✔️已連續簽到${data[account]["status"]["days"]}天</div>`
            // console.log("已連續登入" + data[account]["status"]["days"] + "天")
        }
        else
            insert_text += "&emsp;❌登入失敗<br>";
        console.log(insert_text)
        let status_box = document.getElementById("status_box");
        status_box.insertAdjacentHTML('afterbegin', insert_text);
        // console.log(account);
    }
});